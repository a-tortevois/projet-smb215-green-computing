ts_1 = 0
ts_2 = 0
current = []

def avg(lst):
    return sum(lst) / len(lst)


with open("ina260.csv") as f:
    for line in f:
        value = list(f.readline().strip().split(';'))
        if len(value) > 1:
            if value[1] == '0':
                current.append(float(value[2]))
print(f'Idle: {avg(current)}')

with open("ina260.csv") as f:
    for line in f:
        value = list(f.readline().strip().split(';'))
        #print(f'{value}')
        try:
            if value[1] == '1':
                if ts_1 == 0:
                    ts_1 = int(value[0])
                ts_2 = int(value[0])
                current.append(float(value[2]))
            elif ts_1 != 0:
                print(f'{ts_2-ts_1};{avg(current)}')
                ts_1 = 0
                ts_2 = 0
                current = []
        except IndexError:
            print(f'{value}')
