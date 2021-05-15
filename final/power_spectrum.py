
import board
import busio
import digitalio
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

import time

import numpy as np
from scipy import fft

spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
if spi.try_lock():
    spi.configure(baudrate=1000000)
    spi.unlock()

print(f"frequency: {spi.frequency}")

cs = digitalio.DigitalInOut(board.D5)
mcp = MCP.MCP3008(spi, cs)

channel = AnalogIn(mcp, MCP.P0)

# Calculate the ADC from potentiometer
adc_voltage_fd = open("adc_voltage.csv", "w")
adc_voltage = []
counter = 0
while 1:
    try:
        print(f"ADC Voltage: {channel.voltage} V")
        voltage = channel.voltage
        adc_voltage.append(voltage)
        adc_voltage_fd.write(f"{counter+1},{voltage}\r\n")
        time.sleep(0.1)
        counter += 1
        if counter == 256:
            break
    except KeyboardInterrupt:
        break
adc_voltage_fd.close()

# Calculate FFT and power spectrum
np_adc_voltage = np.array(adc_voltage)
adc_voltage_fft = fft(np_adc_voltage)
power_spec_fd = open("power_spectrum.csv", "w")
counter = 0
for f in adc_voltage_fft:
    data = (f.real * f.real) + (f.imag * f.imag)
    print(data)
    power_spec_fd.write(f"{counter+1},{data}\r\n")
    counter += 1
power_spec_fd.close()
