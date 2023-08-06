#!/usr/bin/env python3
# Author=Hanson
# encoding: utf-8

import time
import serial
import ctypes
import RPi.GPIO as GPIO


class BusServo(object):
    # 幻尔科技总线舵机通信,串口通信命令
    LOBOT_SERVO_FRAME_HEADER = 0x55
    LOBOT_SERVO_MOVE_TIME_WRITE = 1
    LOBOT_SERVO_MOVE_TIME_READ = 2
    LOBOT_SERVO_MOVE_TIME_WAIT_WRITE = 7
    LOBOT_SERVO_MOVE_TIME_WAIT_READ = 8
    LOBOT_SERVO_MOVE_START = 11
    LOBOT_SERVO_MOVE_STOP = 12
    LOBOT_SERVO_ID_WRITE = 13
    LOBOT_SERVO_ID_READ = 14
    LOBOT_SERVO_ANGLE_OFFSET_ADJUST = 17
    LOBOT_SERVO_ANGLE_OFFSET_WRITE = 18
    LOBOT_SERVO_ANGLE_OFFSET_READ = 19
    LOBOT_SERVO_ANGLE_LIMIT_WRITE = 20
    LOBOT_SERVO_ANGLE_LIMIT_READ = 21
    LOBOT_SERVO_VIN_LIMIT_WRITE = 22
    LOBOT_SERVO_VIN_LIMIT_READ = 23
    LOBOT_SERVO_TEMP_MAX_LIMIT_WRITE = 24
    LOBOT_SERVO_TEMP_MAX_LIMIT_READ = 25
    LOBOT_SERVO_TEMP_READ = 26
    LOBOT_SERVO_VIN_READ = 27
    LOBOT_SERVO_POS_READ = 28
    LOBOT_SERVO_OR_MOTOR_MODE_WRITE = 29
    LOBOT_SERVO_OR_MOTOR_MODE_READ = 30
    LOBOT_SERVO_LOAD_OR_UNLOAD_WRITE = 31
    LOBOT_SERVO_LOAD_OR_UNLOAD_READ = 32
    LOBOT_SERVO_LED_CTRL_WRITE = 33
    LOBOT_SERVO_LED_CTRL_READ = 34
    LOBOT_SERVO_LED_ERROR_WRITE = 35
    LOBOT_SERVO_LED_ERROR_READ = 36

    # 发送和接受Board接口
    rx_pin = 33
    tx_pin = 35

    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        self.serialHandle = serial.Serial("/dev/ttyAMA0", 115200)  # 初始化串口， 波特率为115200

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

    @staticmethod
    def checksum(buf):
        # 计算校验和
        sum = 0x00
        for b in buf:  # 求和
            sum += b
        sum = sum - 0x55 - 0x55  # 去掉命令开头的两个 0x55
        sum = ~sum  # 取反
        return sum & 0xff

    def serial_serro_wirte_cmd(self, id=None, w_cmd=None, dat1=None, dat2=None):
        '''
        写指令
        :param id:
        :param w_cmd:
        :param dat1:
        :param dat2:
        :return:
        '''
        self.portWrite()
        buf = bytearray(b'\x55\x55')  # 帧头
        buf.append(id)
        # 指令长度
        if dat1 is None and dat2 is None:
            buf.append(3)
        elif dat1 is not None and dat2 is None:
            buf.append(4)
        elif dat1 is not None and dat2 is not None:
            buf.append(7)

        buf.append(w_cmd)  # 指令
        # 写数据
        if dat1 is None and dat2 is None:
            pass
        elif dat1 is not None and dat2 is None:
            buf.append(dat1 & 0xff)  # 偏差
        elif dat1 is not None and dat2 is not None:
            buf.extend([(0xff & dat1), (0xff & (dat1 >> 8))])  # 分低8位 高8位 放入缓存
            buf.extend([(0xff & dat2), (0xff & (dat2 >> 8))])  # 分低8位 高8位 放入缓存
        # 校验和
        buf.append(self.checksum(buf))
        # for i in buf:
        #     print('%x' %i)
        self.serialHandle.write(buf)  # 发送

    def serial_servo_read_cmd(self, id=None, r_cmd=None):
        '''
        发送读取命令
        :param id:
        :param r_cmd:
        :param dat:
        :return:
        '''
        self.portWrite()
        buf = bytearray(b'\x55\x55')  # 帧头
        buf.append(id)
        buf.append(3)  # 指令长度
        buf.append(r_cmd)  # 指令
        buf.append(self.checksum(buf))  # 校验和
        self.serialHandle.write(buf)  # 发送
        time.sleep(0.00034)

    def serial_servo_get_rmsg(self, cmd):
        '''
        # 获取指定读取命令的数据
        :param cmd: 读取命令
        :return: 数据
        '''
        self.serialHandle.flushInput()  # 清空接收缓存
        self.portRead()  # 将单线串口配置为输入
        time.sleep(0.005)  # 稍作延时，等待接收完毕
        count = self.serialHandle.inWaiting()  # 获取接收缓存中的字节数
        if count != 0:  # 如果接收到的数据不空
            recv_data = self.serialHandle.read(count)  # 读取接收到的数据
            # for i in recv_data:
            #     print('%#x' %ord(i))
            # 是否是读id指令
            try:
                if recv_data[0] == 0x55 and recv_data[1] == 0x55 and recv_data[4] == cmd:
                    dat_len = recv_data[3]
                    self.serialHandle.flushInput()  # 清空接收缓存
                    if dat_len == 4:
                        # print ctypes.c_int8(ord(recv_data[5])).value    # 转换成有符号整型
                        return recv_data[5]
                    elif dat_len == 5:
                        pos = 0xffff & (recv_data[5] | (0xff00 & (recv_data[6] << 8)))
                        return ctypes.c_int16(pos).value
                    elif dat_len == 7:
                        pos1 = 0xffff & (recv_data[5] | (0xff00 & (recv_data[6] << 8)))
                        pos2 = 0xffff & (recv_data[7] | (0xff00 & (recv_data[8] << 8)))
                        return ctypes.c_int16(pos1).value, ctypes.c_int16(pos2).value
                else:
                    return None
            except BaseException as e:
                print(e)
        else:
            self.serialHandle.flushInput()  # 清空接收缓存
            return None

    # 以下实现具体舵机功能
    # 蜂鸣器功能
    # def setBuzzer(new_state):
    #     GPIO.setup(33, GPIO.OUT)
    #     GPIO.output(33, new_state)

    def setBusServoID(self, oldid, newid):
        """
        配置舵机id号, 出厂默认为1
        :param oldid: 原来的id， 出厂默认为1
        :param newid: 新的id
        """
        self.serial_serro_wirte_cmd(oldid, self.LOBOT_SERVO_ID_WRITE, newid)

    def getBusServoID(self, id=None):
        """
        读取串口舵机id
        :param id: 默认为空
        :return: 返回舵机id
        """

        while True:
            if id is None:  # 总线上只能有一个舵机
                self.serial_servo_read_cmd(0xfe, self.LOBOT_SERVO_ID_READ)
            else:
                self.serial_servo_read_cmd(id, self.LOBOT_SERVO_ID_READ)
            # 获取内容
            msg = self.serial_servo_get_rmsg(self.LOBOT_SERVO_ID_READ)
            if msg is not None:
                return msg

    def setBusServoPulse(self, id, pulse, use_time):
        """
        驱动串口舵机转到指定位置
        :param id: 要驱动的舵机id
        :pulse: 位置
        :use_time: 转动需要的时间
        """

        pulse = 0 if pulse < 0 else pulse
        pulse = 1000 if pulse > 1000 else pulse
        use_time = 0 if use_time < 0 else use_time
        use_time = 30000 if use_time > 30000 else use_time
        self.serial_serro_wirte_cmd(id, self.LOBOT_SERVO_MOVE_TIME_WRITE, pulse, use_time)

    def stopBusServo(self, id=None):
        '''
        停止舵机运行
        :param id:
        :return:
        '''
        self.serial_serro_wirte_cmd(id, self.LOBOT_SERVO_MOVE_STOP)

    def setBusServoDeviation(self, id, d=0):
        """
        调整偏差
        :param id: 舵机id
        :param d:  偏差
        """
        self.serial_serro_wirte_cmd(id, self.LOBOT_SERVO_ANGLE_OFFSET_ADJUST, d)

    def saveBusServoDeviation(self, id):
        """
        配置偏差，掉电保护
        :param id: 舵机id
        """
        self.serial_serro_wirte_cmd(id, self.LOBOT_SERVO_ANGLE_OFFSET_WRITE)

    def getBusServoDeviation(self, id):
        '''
        读取偏差值
        :param id: 舵机号
        :return:
        '''
        # 发送读取偏差指令
        count = 0
        while True:
            self.serial_servo_read_cmd(id, self.LOBOT_SERVO_ANGLE_OFFSET_READ)
            # 获取
            msg = self.serial_servo_get_rmsg(self.LOBOT_SERVO_ANGLE_OFFSET_READ)
            count += 1
            if msg is not None:
                return msg
            # 超时时间
            if count > 50:
                return None

    def setBusServoAngleLimit(self, id, low, high):
        '''
        设置舵机转动范围
        :param id:
        :param low:
        :param high:
        :return:
        '''
        self.serial_serro_wirte_cmd(id, self.LOBOT_SERVO_ANGLE_LIMIT_WRITE, low, high)

    def getBusServoAngleLimit(self, id):
        '''
        读取舵机转动范围
        :param id:
        :return: 返回元祖 0： 低位  1： 高位
        '''

        while True:
            self.serial_servo_read_cmd(id, self.LOBOT_SERVO_ANGLE_LIMIT_READ)
            msg = self.serial_servo_get_rmsg(self.LOBOT_SERVO_ANGLE_LIMIT_READ)
            if msg is not None:
                count = 0
                return msg

    def setBusServoVinLimit(self, id, low, high):
        '''
        设置舵机电压范围
        :param id:
        :param low:
        :param high:
        :return:
        '''
        self.serial_serro_wirte_cmd(id, self.LOBOT_SERVO_VIN_LIMIT_WRITE, low, high)

    def getBusServoVinLimit(self, id):
        '''
        读取舵机转动范围
        :param id:
        :return: 返回元祖 0： 低位  1： 高位
        '''
        while True:
            self.serial_servo_read_cmd(id, self.LOBOT_SERVO_VIN_LIMIT_READ)
            msg = self.serial_servo_get_rmsg(self.LOBOT_SERVO_VIN_LIMIT_READ)
            if msg is not None:
                return msg

    def setBusServoMaxTemp(self, id, m_temp):
        '''
        设置舵机最高温度报警
        :param id:
        :param m_temp:
        :return:
        '''
        self.serial_serro_wirte_cmd(id, self.LOBOT_SERVO_TEMP_MAX_LIMIT_WRITE, m_temp)

    def getBusServoTempLimit(self, id):
        '''
        读取舵机温度报警范围
        :param id:
        :return:
        '''

        while True:
            self.serial_servo_read_cmd(id, self.LOBOT_SERVO_TEMP_MAX_LIMIT_READ)
            msg = self.serial_servo_get_rmsg(self.LOBOT_SERVO_TEMP_MAX_LIMIT_READ)
            if msg is not None:
                return msg

    def getBusServoPulse(self, id):
        '''
        读取舵机当前位置
        :param id:
        :return:
        '''
        while True:
            self.serial_servo_read_cmd(id, self.LOBOT_SERVO_POS_READ)
            msg = self.serial_servo_get_rmsg(self.LOBOT_SERVO_POS_READ)
            if msg is not None:
                return msg

    def getBusServoTemp(self, id):
        '''
        读取舵机温度
        :param id:
        :return:
        '''
        while True:
            self.serial_servo_read_cmd(id, self.LOBOT_SERVO_TEMP_READ)
            msg = self.serial_servo_get_rmsg(self.LOBOT_SERVO_TEMP_READ)
            if msg is not None:
                return msg

    def getBusServoVin(self, id):
        '''
        读取舵机电压
        :param id:
        :return:
        '''
        while True:
            self.serial_servo_read_cmd(id, self.LOBOT_SERVO_VIN_READ)
            msg = self.serial_servo_get_rmsg(self.LOBOT_SERVO_VIN_READ)
            if msg is not None:
                return msg

    def restBusServoPulse(self, oldid):
        # 舵机清零偏差和P值中位（500）
        self.serial_servo_set_deviation(oldid, 0)  # 清零偏差
        time.sleep(0.1)
        self.serial_serro_wirte_cmd(oldid, self.LOBOT_SERVO_MOVE_TIME_WRITE, 500, 100)  # 中位

    # 掉电
    def unloadBusServo(self, id):
        self.serial_serro_wirte_cmd(id, self.LOBOT_SERVO_LOAD_OR_UNLOAD_WRITE, 0)

    # 读取是否掉电
    def getBusServoLoadStatus(self, id):
        while True:
            self.serial_servo_read_cmd(id, self.LOBOT_SERVO_LOAD_OR_UNLOAD_READ)
            msg = self.serial_servo_get_rmsg(self.LOBOT_SERVO_LOAD_OR_UNLOAD_READ)
            if msg is not None:
                return msg

    # setBuzzer(0)


if __name__ == "__main__":
    print("功能:幻尔科技TonyPi扩展板，串口舵机读取状态例程")
    object1 = BusServo()


    def getBusServoStatus(id):
        Pulse = object1.getBusServoPulse(id)  # 获取19号舵机的位置信息
        Temp = object1.getBusServoTemp(id)  # 获取19号舵机的温度信息
        Vin = object1.getBusServoVin(id)  # 获取19号舵机的电压信息
        print('Pulse: {}\nTemp:  {}℃\nVin:   {}mV\n'.format(Pulse, Temp, Vin))  # 打印状态信息
        time.sleep(0.5)  # 延时方便查看


    getBusServoStatus(19)

    # while True:
    #     object1.setBusServoPulse(8, 500, 1000) # 8号舵机转到500位置用时1000ms
    #     time.sleep(1)
    #     getBusServoStatus()
    #     object1.setBusServoPulse(8, 300, 1000)
    #     time.sleep(1)
    #     getBusServoStatus()
