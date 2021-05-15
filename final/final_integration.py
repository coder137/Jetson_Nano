
import board
import busio
import digitalio
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import Jetson.GPIO as GPIO

import time


# DIR = 18
# STEP = 32
# ENABLE = 15
# MS2 = 12
# MS1 = 11

MAX_MOTOR_FREQUENCY = 2000
MAX_POTENTIOMETER_RANGE = 65535
DUTY_CYCLE = 50
DIR = board.D24
STEP = board.D12
ENABLE = board.D22
MS2 = board.D18
MS1 = board.D17


spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
cs = digitalio.DigitalInOut(board.D5)
dir = digitalio.DigitalInOut(DIR)
step = digitalio.DigitalInOut(STEP)
enable = digitalio.DigitalInOut(ENABLE)
ms2 = digitalio.DigitalInOut(MS2)
ms1 = digitalio.DigitalInOut(MS1)


def reset_pins():
    dir.value = False
    step.value = False
    ms2.value = False
    ms1.value = False
    enable.value = True


def setup():
    dir.direction = digitalio.Direction.OUTPUT
    step.direction = digitalio.Direction.OUTPUT
    enable.direction = digitalio.Direction.OUTPUT
    ms1.direction = digitalio.Direction.OUTPUT
    ms2.direction = digitalio.Direction.OUTPUT
    reset_pins()
    print("Begin motor control")


def pwm(frequency, dutycycle):
    if frequency <= 1:
        step.value = False
        time.sleep(0.5)
        return

    one_cycle = 1/frequency
    on_time = (dutycycle * one_cycle) / 100
    off_time = one_cycle - on_time
    step.value = True
    time.sleep(on_time)
    step.value = False
    time.sleep(off_time)


# Start the program here
print("Starting")
setup()

if spi.try_lock():
    spi.configure(baudrate=1000000)
    spi.unlock()
print(f"spi frequency: {spi.frequency}")
mcp = MCP.MCP3008(spi, cs)

channel = AnalogIn(mcp, MCP.P0)

while 1:
    try:
        # print(f"Raw ADC Value: {channel.value}")
        # print(f"ADC Voltage: {channel.voltage} V")

        # 65535 -> 2000
        # x -> y
        # x * 2000 / 65535
        frequency = int((channel.value * MAX_MOTOR_FREQUENCY) /
                        MAX_POTENTIOMETER_RANGE)
        print(frequency)
        pwm(frequency, DUTY_CYCLE)
    except KeyboardInterrupt:
        break
