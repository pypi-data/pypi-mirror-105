#!/usr/bin/python
# Author=Hanson
# encoding: utf-8

import time
import serial
import RPi.GPIO as GPIO


class BusServo(object):

    # 发送和接受Board接口
    rx_pin = 33  # 对应6号舵机
    tx_pin = 35  # 对应5号舵机

    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        self.serialHandle = serial.Serial("/dev/ttyAMA0", 115200)  # 初始化串口， 波特率为115200
        # print(self.serialHandle.is_open)
        # 初始化串口
        GPIO.setup(self.rx_pin, GPIO.OUT)
        GPIO.output(self.rx_pin, 0)  # 配置RX_CON为输入
        GPIO.setup(self.tx_pin, GPIO.OUT)
        GPIO.output(self.tx_pin, 1)  # 配置TX_CON为输出

    def portWrite(self):  # 配置单线串口为输出
        GPIO.output(self.tx_pin, 1)  # 拉高TX_CON 即 GPIO27
        GPIO.output(self.rx_pin, 0)  # 拉低RX_CON 即 GPIO17

    def portRead(self):  # 配置单线串口为输入
        GPIO.output(self.rx_pin, 1)  # 拉高RX_CON 即 GPIO17
        GPIO.output(self.tx_pin, 0)  # 拉低TX_CON 即 GPIO27

    def portRest(self):
        time.sleep(0.1)
        self.serialHandle.close()
        GPIO.output(self.rx_pin, 1)
        GPIO.output(self.tx_pin, 1)
        self.serialHandle.open()
        time.sleep(0.1)

    def serial_servo_wirte_cmd(self, data_cmd=None):
        # 写指令:param data
        self.portWrite()  # 将单线串口配置为输出
        print('serial sending ...')
        self.serialHandle.write(data_cmd.encode("utf-8"))  # 发送
        self.portRest()
        # # self.serialHandle.flushInput()  # 清空接收缓存
        # self.portRead()  # 将单线串口配置为输入
        # print('serial receiveing ...')
        # time.sleep(0.005)  # 稍作延时，等待接收完毕
        # count = self.serialHandle.inWaiting()  # 获取接收缓存中的字节数
        # # return count
        # if count != 0:  # 如果接收到的数据不空
        #     recv_data = self.serialHandle.read(count)  # 读取接收到的数据
        #     return recv_data
        # self.serialHandle.close()

    def serial_servo_get_message(self):
        while True:
            # self.serialHandle.flushInput()  # 清空接收缓存
            self.portRead()  # 将单线串口配置为输入
            print('serial receiveing ...')
            time.sleep(0.005)  # 稍作延时，等待接收完毕
            time.sleep(1)
            count = self.serialHandle.inWaiting()  # 获取接收缓存中的字节数
            if count != 0:  # 如果接收到的数据不空
                recv_data = self.serialHandle.read(count)  # 读取接收到的数据
                return recv_data

            # self.serialHandle.close()


if __name__ == "__main__":
    print("功能:幻尔科技TonyPi扩展板，串口舵机读取状态例程")
    object1 = BusServo()
    # object1.serial_servo_wirte_cmd("111")
    res = object1.serial_servo_get_message()
    print(res)

    # def getBusServoStatus(id):
    #     Pulse = object1.getBusServoPulse(id)  # 获取19号舵机的位置信息
    #     Temp = object1.getBusServoTemp(id)  # 获取19号舵机的温度信息
    #     Vin = object1.getBusServoVin(id)  # 获取19号舵机的电压信息
    #     print('Pulse: {}\nTemp:  {}℃\nVin:   {}mV\n'.format(Pulse, Temp, Vin))  # 打印状态信息
    #     time.sleep(0.5)  # 延时方便查看
    #
    #
    # getBusServoStatus(19)

    # while True:
    #     object1.setBusServoPulse(8, 500, 1000) # 8号舵机转到500位置用时1000ms
    #     time.sleep(1)
    #     getBusServoStatus()
    #     object1.setBusServoPulse(8, 300, 1000)
    #     time.sleep(1)
    #     getBusServoStatus()
