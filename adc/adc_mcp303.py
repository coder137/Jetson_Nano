
import board
import busio
import digitalio
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

import time


spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
if spi.try_lock():
    spi.configure(baudrate=1000000)
    spi.unlock()

print(f"frequency: {spi.frequency}")

cs = digitalio.DigitalInOut(board.D5)
mcp = MCP.MCP3008(spi, cs)

channel = AnalogIn(mcp, MCP.P0)

while 1:
    try:
        print(f"Raw ADC Value: {channel.value}")
        print(f"ADC Voltage: {channel.voltage} V")
        time.sleep(1)
    except KeyboardInterrupt:
        break
