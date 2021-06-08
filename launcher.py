'''
root@raspberrypi:~/projet-smb215# taskset -c 0 python3 launcher.py 10 algo-01 py
root@raspberrypi:~/projet-smb215# taskset -c 0 python3 launcher.py 10 algo-03-r2 > algo-03-r2-stdout.txt
'''

import RPi.GPIO as GPIO
import os
import re
import subprocess
import sys
import time

# IO Config
PIN_SYNC = 23
PIN_IS_RUN = 24
OPEN = GPIO.HIGH
CLOSE = GPIO.LOW

DIR = os.path.dirname(os.path.abspath(__file__))
PERF = 'perf'
MEM = 'mem'
DELAY = 5
DEBUG = True

ALL_EXT = ['class', 'o', 'js', 'php', 'py']

path = ''
count = 0
ext_to_test = []


def exit(error=''):
	if error != '':
		print(f'{error}\n')
		usage()
		sys.exit(1)

	sys.exit(0)


def usage():
	print(f'Usage: \n')


def debug(message):
	if DEBUG:
		print(f'{message}\n')


def file_exists(file):
	if not file:
		return False
	else:
		return os.path.isfile(os.path.join(path, file))


def build():
	java = []
	for file in os.listdir(path):
		if file.endswith(".c"):
			filename = file.split('.')[0]
			debug(f'Build {filename}.o')
			run_command(f'gcc -w -Wall {path}/{filename}.c -o {path}/{filename}.o')

	if file_exists('ArtOptimal.java') and file_exists('DrawableArea.java'):
		debug(f'Build DrawableArea.class ArtOptimal.class')
		run_command(f'javac {path}/DrawableArea.java {path}/ArtOptimal.java')
	elif file_exists('ArtOptimal.java'):
		debug(f'Build ArtOptimal.class')
		run_command(f'javac {path}/ArtOptimal.java')
	return 0


def initialize_result_file():
	for type in [PERF, MEM]:
		file = f'{DIR}/{path}/{type}.csv'
		if file_exists(file):
			os.remove(file)
		# create with headers
		with open(file, 'a') as f:
			f.write(f'lang;filename;i;{";".join(get_header(type))}\n')
			f.close()


def get_header(type):
	if type == PERF:
		return [
			'task_clock_1',
			'task_clock_2',
			'context_switches_1',
			'context_switches_2',
			'cpu_migrations_1',
			'cpu_migrations_2',
			'page_faults_1',
			'page_faults_2',
			'cycles_1',
			'cycles_2',
			'instructions_1',
			'instructions_2',
			'branches_1',
			'branches_2',
			'branch_misses_1',
			'branch_misses_2',
			'L1_dcache_loads_1',
			'L1_dcache_loads_2',
			'L1_dcache_load_misses_1',
			'L1_dcache_load_misses_2',
			'LLC_loads_1',
			'LLC_loads_2',
			'LLC_load_misses_1',
			'LLC_load_misses_2',
			'time',
		]
	elif type == MEM:
		return [
			'user_time',
			'system_time',
			'cpu',
			'clock_time',
			'size_1',
			'size_2',
			'size_3',
			'size_4',
			'max_set_size',
			'avg_set_size',
			'major_page_faults',
			'minor_page_faults',
			'context_switches_1',
			'context_switches_2',
			'swaps',
			'fs_inputs',
			'fs_outputs',
			'socket_sent',
			'socket_received',
			'signals',
			'page_size',
			'exit_status',
		]
	else:
		raise Exception('get_header: unknown type')


def get_command(type, path, file):
	if type == PERF:
		cmd = '/usr/bin/perf stat -d -- taskset -c 0'
	elif type == MEM:
		cmd = '/usr/bin/time -v taskset -c 0'
	else:
		raise Exception('get_command: unknown type')

	ext = file.split('.')[1]
	if 'class' in ext_to_test and file.split('.')[0] == "ArtOptimal" and ext == 'class':
		javaClass = file.split('.')[0]
		return f'{cmd} java -cp {path} {javaClass}'
	if 'o' in ext_to_test and ext == 'o':
		return f'{cmd} ./{path}/{file}'
	if 'js' in ext_to_test and ext == 'js':
		return f'{cmd} node {path}/{file}'
	if 'php' in ext_to_test and ext == 'php':
		return f'{cmd} php -f {path}/{file}'
	if 'py' in ext_to_test and ext == 'py':
		return f'{cmd} python3 {path}/{file}'
	return ''


def run_command(cmd):
	GPIO.output(PIN_IS_RUN, CLOSE)
	process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)  # , universal_newlines=True)
	stdout, stderr = process.communicate()
	GPIO.output(PIN_IS_RUN, OPEN)
	output = stdout.decode('utf-8')
	debug(f'stdout: {output}\n')
	return output


def parse_output(type, stdout):
	stdout = stdout.replace(',', '')
	if type == PERF:
		matches = re.findall('[ \t]+([0-9]+[\.]*[0-9]*)', stdout, re.MULTILINE | re.IGNORECASE)
	elif type == MEM:
		matches = re.findall('[ \t]+([0-9]*[:]*[0-9]+[\.]*[0-9]*)', stdout, re.MULTILINE | re.IGNORECASE)
	else:
		raise Exception('parse_output: unknown type')
	return matches[2::]


def save(type, lang, filename, i, result):
	file = f'{path}/{type}.csv'
	with open(file, 'a') as f:
		f.write(f'{lang};{filename};{i};{";".join(result)}\n')
		f.close()


def main():
	# Define I/O
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(PIN_SYNC, GPIO.OUT, initial=CLOSE)
	GPIO.setup(PIN_IS_RUN, GPIO.OUT, initial=OPEN)
	# Start
	# build()
	initialize_result_file()
	#for root, dirs, files in os.walk(path):
	#debug(f'root: {root}, dirs: {dirs}, files: {files}\n')
	files = []
	if path == 'algo-01':
		files = ['art-optimal.o','ArtOptimal.class','art-optimal.js','art-optimal.php','art-optimal.py']		
	elif path == 'algo-02':
		files = ['art-optimal-origin.o','art-optimal-linkedlist.o','ArtOptimal.class','art-optimal.js','art-optimal.php','art-optimal-origin.py','art-optimal-optim.py']
	elif path == 'algo-03-r1' :
		files = ['art-optimal.o','ArtOptimal.class','art-optimal.js','art-optimal.php','art-optimal.py']
	elif path == 'algo-03-r2' :
		files = ['art-optimal.js'] # 'art-optimal.o','ArtOptimal.class',,'art-optimal.php','art-optimal.py'
	for file in files:
		if file_exists(file):
			filename = file.split('.')[0]
			lang = file.split('.')[1]
			for type in [PERF, MEM]:
				cmd = get_command(type, path, file)
				if cmd == '':
					continue
				for i in range(1, count):
					debug(f'{i}: {cmd}')
					result = parse_output(type, run_command(cmd))
					debug(f'result: {result}\n')
					save(type, lang, filename, i, result)
					time.sleep(DELAY)
	GPIO.output(PIN_SYNC, OPEN)
	GPIO.cleanup()


if __name__ == '__main__':
	if len(sys.argv) < 3:
		exit('Error: arg length error')

	match = re.search('^([0-9]*)$', sys.argv[1], re.IGNORECASE)
	if not match:
		exit('Error: arg[1] is not a number')

	if not os.path.exists(os.path.join(DIR, sys.argv[2])):
		exit('Error: arg[2] is not a valid directory')

	if len(sys.argv) > 3:
		ext_to_test.extend(sys.argv[3::])
	else:
		ext_to_test = ALL_EXT

	#debug(f'ext_to_test: {ext_to_test}')

	count = int(sys.argv[1]) + 1
	path = sys.argv[2]

try:
	main()
except KeyboardInterrupt:
	GPIO.output(PIN_SYNC, OPEN)
	GPIO.output(PIN_IS_RUN, OPEN)
	GPIO.cleanup()
