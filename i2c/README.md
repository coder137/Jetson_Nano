# I2C on Jetson Nano

- Target platform: **Jetson Nano 2GB** with **CircuitPython adafruit blinka** module

# Links

- [I2C Circuit Python](https://learn.adafruit.com/circuitpython-libraries-on-linux-and-the-nvidia-jetson-nano?view=all)
- [Jetson Nano 2GB pinout diagram](https://developer.nvidia.com/embedded/learn/jetson-nano-2gb-devkit-user-guide)

# Installing

- [Jetson GPIO](https://github.com/NVIDIA/jetson-gpio)
- `pip3 install adafruit-blinka`

# Testing

- `python3 i2c_lsm303.py`
- Output will appear in console via print statements

# I2C basics on Jetson Nano

- We can use raw queries on the i2c port on Jetson Nano using ioctl commands to `dev/i2c`.
- These can be cumbersome which is why we use the circuit-python `adafruit-blinka` package to handle this under the hood

## Opening and Closing

```python
import busio
# Open the i2c port
i2c = busio.I2C(SCL_PIN, SDA_PIN)

# Use the i2c port here
# ...

# Close th i2c port
i2c.deinit()
```

## Scanning

```python
# Get the 7 bit address of the device
connected_devices = i2c.scan()
for device in connected_devices:
    print(f"Device: {hex(device)}")
```

## Write + Read

```python
# Write data over i2c
i2c.writeto(DEVICE_ADDRESS, bytes([DEVICE_REGISTER, data]))

# Read 2 bytes of data over i2c
read_data = byteaddress(2)
i2c.readFrom(DEVICE_ADDRESS, read_data)
```

## R/W Combined

```python
# Write then read from address
# Stop transaction after this transaction is completed
read_data = byte_address(BYTE_NUMS)
i2c.writeto_then_readfrom(DEVICE_ADDRESS, bytes([DEVICE_REGISTER, data]), read_data, stop=True)
```

# Interfacing with LSM303DLHC

## Init Accelerometer

- In `CTRL_REG1_A: 0x20` register we set
  - ODR[3:0] to 9
  - LPen to 0
  - Xen, Yen and Zen to 1
  - `9 << 4 | (1 << 0) | (1 << 1) | (1 << 2)`
  - This sets the accelerometer in Normal mode with 1.344Khz data rate
- In `CTRL_REG4_A: 0x23` register we set
  - HR to 1
  - `1 << 3`
  - HR stands for High resolution mode to get 16 bit output from accelerometer
- Check the `init` function in `i2c_lsm303.py`

## Read Accelerometer

- `OUT_X_H_A` is 0x28
- `OUT_X_L_A` is 0x29
- `OUT_Y_H_A` is 0x2A
- `OUT_Y_L_A` is 0x2B
- `OUT_Z_H_A` is 0x2C
- `OUT_Z_L_A` is 0x2D

- We use the R/W combined I2C API to read raw X, Y, Z accelerometer values
```python
read_acc = bytearray(6)
i2c.writeto_then_readfrom(ACC_DEVICE_ADDRESS, bytes(
    [OUT_X_L_A]), read_acc, stop=True)
```
- `OUT_X_L_A` is `0x28`

## Init Magnetometer and Temperature

- We set `CRA_REG_M` 
  - `TEMP_EN` to 1
  - `DO` Data rate `0b100` i.e 15 hz
```python
cra_reg_m = (1 << 7) | (0x4 << 2)
i2c.writeto(MAG_DEVICE_ADDRESS, bytes([CRA_REG_M, cra_reg_m]))
```

## Read Magnetometer

- `OUT_X_H_M` is 0x03
- `OUT_X_L_M` is 0x04
- `OUT_Z_H_M` is 0x05
- `OUT_Z_L_M` is 0x06
- `OUT_Y_H_M` is 0x07
- `OUT_Y_L_M` is 0x08

```python
read_mag = bytearray(6)
i2c.writeto_then_readfrom(MAG_DEVICE_ADDRESS, bytes(
    [OUT_X_H_M]), read_mag, stop=True)
```

## Read Temperature

- `TEMP_OUT_H_M` is 0x31
- `TEMP_OUT_L_M` is 0x32

```python
read_temp = bytearray(2)
i2c.writeto_then_readfrom(MAG_DEVICE_ADDRESS, bytes(
    [TEMP_OUT_H_M]), read_temp, stop=True)
```
