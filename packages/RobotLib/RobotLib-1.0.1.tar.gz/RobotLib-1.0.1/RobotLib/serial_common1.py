# -*- coding: utf-8 -*
import serial
import time

ser = serial.Serial('/dev/ttyAMA0', 115200)
# print(ser.isOpen())
# if ser.isOpen == False:
#     ser.open()  # 打开串口
# ser.write(b"Raspberry pi is ready")


def write_cmd():
    try:
        while True:
            input_data = input("enter cmd in serial:")
            ser.write(input_data.encode("utf-8"))
    except KeyboardInterrupt:
        ser.close()


def get_message():
    try:
        while True:
            size = ser.inWaiting()  # 获得缓冲区字符
            if size != 0:
                response = ser.read(size)  # 读取内容并显示
                print(response)
                ser.flushInput()  # 清空接收缓存区
                time.sleep(0.1)  # 软件延时
    except KeyboardInterrupt:
        ser.close()


def cmd_get_message():
    try:
        while True:
            size = ser.inWaiting()  # 获得缓冲区字符
            if size != 0:
                response = ser.read(size)  # 读取内容并显示
                print(type(response), response)
                print(str(response, encoding="gbk"))
                ser.flushInput()  # 清空接收缓存区
                time.sleep(0.1)  # 软件延时
            input_data = input("enter cmd in serial:")
            ser.write(input_data.encode("utf-8"))
    except KeyboardInterrupt:
        ser.close()


if __name__ == "__main__":
    print("串口测试")
    # write_cmd()
    # get_message()
    cmd_get_message()
