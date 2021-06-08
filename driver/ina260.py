#!/usr/bin/env python3
import ctypes
import datetime
import sys
import time
import RPi.GPIO as GPIO

try:
    import smbus
except ImportError as e:
    print('SMBUS is not installed, Please install and Try again.')
    sys.exit(0)

# IO Config
PIN_SYNC = 23
PIN_IS_RUN = 24
IS_RUN = 0
IS_SYNC = 0
DELAY = 0.5  # 5 / 1000

INA260_ADDRESS = (0x40)
INA260_I2C_BUS_NUMBER = 1

INA260_REG_CONFIG = (0x00)
INA260_REG_CURRENT = (0x01)
INA260_REG_VOLTAGE = (0x02)
INA260_REG_POWER = (0x03)
INA260_REG_MASKENABLE = (0x06)
INA260_REG_ALERTLIMIT = (0x07)

INA260_Avg = dict(
    INA260_AVG_1=0b000,
    INA260_AVG_4=0b001,
    INA260_AVG_16=0b010,
    INA260_AVG_64=0b011,
    INA260_AVG_128=0b100,
    INA260_AVG_256=0b101,
    INA260_AVG_512=0b110,
    INA260_AVG_1024=0b111)

INA260_ConvTime = dict(
    INA260_CONV_TIME_140US=0b000,
    INA260_CONV_TIME_204US=0b001,
    INA260_CONV_TIME_332US=0b010,
    INA260_CONV_TIME_588US=0b011,
    INA260_CONV_TIME_1100US=0b100,
    INA260_CONV_TIME_2116US=0b101,
    INA260_CONV_TIME_4156US=0b110,
    INA260_CONV_TIME_8244US=0b111)

INA260_Mode = dict(
    INA260_MODE_POWER_DOWN=0b000,
    INA260_MODE_SHUNT_TRIG=0b001,
    INA260_MODE_BUS_TRIG=0b010,
    INA260_MODE_SHUNT_BUS_TRIG=0b011,
    INA260_MODE_ADC_OFF=0b100,
    INA260_MODE_SHUNT_CONT=0b101,
    INA260_MODE_BUS_CONT=0b110,
    INA260_MODE_SHUNT_BUS_CONT=0b111)


class ina260:
    def __init__(self, INA260_addr=INA260_ADDRESS, i2c_bus_number=INA260_I2C_BUS_NUMBER):
        self.INA260_addr = INA260_addr
        self.i2c_bus = smbus.SMBus(i2c_bus_number)

    def _read(self, register):
        data = self.i2c_bus.read_i2c_block_data(self.INA260_addr, register, 2)
        return ctypes.c_int16(data[0] << 8 | data[1]).value

    def _write(self, register, data):
        self.i2c_bus.write_i2c_block_data(self.INA260_addr, register, [(data >> 8), (data & 0xFF)])

    def configure(self, avg=INA260_Avg['INA260_AVG_4'], busConvTime=INA260_ConvTime['INA260_CONV_TIME_588US'], shuntConvTime=INA260_ConvTime['INA260_CONV_TIME_588US'],
                  mode=INA260_Mode['INA260_MODE_SHUNT_BUS_CONT']):
        config = 0
        config |= (avg << 9 | busConvTime << 6 | shuntConvTime << 3 | mode)
        self._write(INA260_REG_CONFIG, config)

    def getMode(self):
        value = self._read(INA260_REG_CONFIG)
        value &= 0x07
        return value

    def readCurrent(self):
        return round(self._read(INA260_REG_CURRENT) * 0.00125, 5)

    def readVoltage(self):
        return round(self._read(INA260_REG_VOLTAGE) * 0.00125, 5)

    def readPower(self):
        return round(self._read(INA260_REG_POWER) * 0.01, 2)

    def close(self):
        self.i2c_bus.close()


def printf(format, *args):
    sys.stdout.write(format % args)


def onIsSyncEvent(channel):
    global IS_SYNC
    if GPIO.input(channel):
        # Open
        print(f'IS_SYNC Open')
        IS_SYNC = 0
    else:
        # Close
        print(f'IS_SYNC Close')
        IS_SYNC = 1


def onIsRunEvent(channel):
    global IS_RUN
    if GPIO.input(channel):
        # Open
        IS_RUN = 0
    else:
        # Close
        IS_RUN = 1


def main():
    # Define I/O
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN_SYNC, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(PIN_IS_RUN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(PIN_SYNC, GPIO.BOTH, callback=onIsSyncEvent)
    GPIO.add_event_detect(PIN_IS_RUN, GPIO.BOTH, callback=onIsRunEvent)

    sensor = ina260()
    print('Configuring INA260')
    sensor.configure(avg=INA260_Avg['INA260_AVG_4'], busConvTime=INA260_ConvTime['INA260_CONV_TIME_588US'], shuntConvTime=INA260_ConvTime['INA260_CONV_TIME_588US'],
                     mode=INA260_Mode['INA260_MODE_SHUNT_BUS_CONT'])
    time.sleep(1)
    print('Configuration Done')
    print('Mode is ' + str(hex(sensor.getMode())))
    print('Current: ' + str(sensor.readCurrent()) + 'A')
    print('Voltage: ' + str(sensor.readVoltage()) + 'V')

    while not IS_SYNC:
        time.sleep(0.25)

    while IS_SYNC:
        printf('%s;%s;%s;%s;%s\n', int(datetime.datetime.timestamp(datetime.datetime.now()) * 1000), IS_RUN, sensor.readCurrent(), sensor.readVoltage(), sensor.readPower())
        time.sleep(DELAY)


try:
    main()
except KeyboardInterrupt:
    sensor.close()
    GPIO.cleanup()
