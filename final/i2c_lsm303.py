# Normal mode working
# LPEN = 0
# HR  = 1
# BW ODR = 9
import board
import busio

import time

ACC_DEVICE_ADDRESS = 0x19
MAG_DEVICE_ADDRESS = 0x1e
CTRL_REG1_A = 0x20
CTRL_REG4_A = 0x23
STATUS_REG_A = 0x27
OUT_X_L_A = 0x28

CRA_REG_M = 0x00
CRB_REG_M = 0x01
MR_REG_M = 0x02
OUT_X_H_M = 0x03
SR_REG_M = 0x09
TEMP_OUT_H_M = 0x31


def init(i2c: busio.I2C):
    ctrl_reg1_a_value = ((9 << 4) | (1 << 0) | (1 << 1) | (1 << 2))
    i2c.writeto(ACC_DEVICE_ADDRESS, bytes([CTRL_REG1_A, ctrl_reg1_a_value]))

    ctrl_reg4_a_value = (1 << 3)
    i2c.writeto(ACC_DEVICE_ADDRESS, bytes([CTRL_REG4_A, ctrl_reg4_a_value]))

    cra_reg_m = (1 << 7) | (0x4 << 2)
    i2c.writeto(MAG_DEVICE_ADDRESS, bytes([CRA_REG_M, cra_reg_m]))

    crb_read_m_data = bytearray(1)
    i2c.writeto_then_readfrom(MAG_DEVICE_ADDRESS, bytes(
        [CRB_REG_M]), crb_read_m_data, stop=True)
    print(f"CRB_REG_M: {hex(crb_read_m_data[0])}")

    mr_reg_m = (0)
    i2c.writeto(MAG_DEVICE_ADDRESS, bytes([MR_REG_M, mr_reg_m]))


def get_temp(i2c: busio.I2C) -> int:
    """
    MSB 0x31
    LSB 0x31
    8 LSB / deg - 12 bit resolution
    """
    read_temp = bytearray(2)
    i2c.writeto_then_readfrom(MAG_DEVICE_ADDRESS, bytes(
        [TEMP_OUT_H_M]), read_temp, stop=True)
    # print(f"Raw Temp: {hex(read_temp[0])} : {hex(read_temp[1])}")
    p = (read_temp[0] << 8) | (read_temp[1] >> 3)
    return (p >> 4)


def get_accelerometer(i2c: busio.I2C):
    read_acc = bytearray(6)
    i2c.writeto_then_readfrom(ACC_DEVICE_ADDRESS, bytes(
        [OUT_X_L_A]), read_acc, stop=True)

    # 0x1000 0000
    # print(f"Raw Accelerometer: {hex(read_acc[1])} : {hex(read_acc[0])}")
    # print(f"Raw Accelerometer: {hex(read_acc[3])} : {hex(read_acc[2])}")
    # print(f"Raw Accelerometer: {hex(read_acc[5])} : {hex(read_acc[4])}")

    acc_x = read_acc[1] << 8 | read_acc[0]
    acc_y = read_acc[3] << 8 | read_acc[2]
    acc_z = read_acc[5] << 8 | read_acc[4]

    return (acc_x, acc_y, acc_z)


def get_magnetometer(i2c: busio.I2C):
    read_mag = bytearray(6)
    i2c.writeto_then_readfrom(MAG_DEVICE_ADDRESS, bytes(
        [OUT_X_H_M]), read_mag, stop=True)

    # print(f"Raw Magnetometer: {hex(read_mag[1])} : {hex(read_mag[0])}")
    # print(f"Raw Magnetometer: {hex(read_mag[3])} : {hex(read_mag[2])}")
    # print(f"Raw Magnetometer: {hex(read_mag[5])} : {hex(read_mag[4])}")

    mag_x = read_mag[1] << 8 | read_mag[0]
    mag_z = read_mag[3] << 8 | read_mag[2]
    mag_y = read_mag[5] << 8 | read_mag[4]

    return (mag_x, mag_y, mag_z)


# Main starts here

if __name__ == "__main__":
    # Try to create an I2C device
    i2c = busio.I2C(board.SCL, board.SDA)
    print("I2C 2 ok!")

    list_scanned = i2c.scan()
    for d in list_scanned:
        print(f"Scanned ports: {hex(d)}")

    init(i2c)

    while 1:
        print(f"Temp: {get_temp(i2c)}")
        print(f"Accelerometer: {get_accelerometer(i2c)}")
        print(f"Magnetometer: {get_magnetometer(i2c)}")
        time.sleep(1)

    print("done!")
    i2c.deinit()
