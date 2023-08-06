#!/usr/bin/env python3
# encoding: utf-8
import os
import time
import sqlite3 as sql
from Bus_Servo_Lib import BusServo


class BusServoMotion(object):
    object1 = BusServo()

    def __init__(self):
        # 上位机编辑的动作调用库
        self.runningAction = False
        self.stop_action = False
        self.stop_action_group = False

        self.__end = False
        self.__start = False
        self.current_status = ""

    def stopAction(self):
        self.stop_action = True

    def stopActionGroup(self):
        self.stop_action_group = True

    def runActionGroup(self, actName, times=1, with_stand=False, lock_servos=''):

        temp = times
        while True:
            if temp != 0:
                times -= 1
            try:
                if (
                        actName != 'go_forward' and actName != 'go_forward_fast' and actName != 'go_forward_slow' and actName != 'back' and actName != 'back_fast') or stop_action_group:
                    if self.__end:
                        self.__end = False
                        if self.current_status == 'go':
                            self.runAction('go_forward_end', lock_servos)
                        else:
                            self.runAction('back_end', lock_servos)
                        # print('end2')
                    if self.stop_action_group:
                        self.__end = False
                        self.__start = True
                        self.stop_action_group = False
                        # print('stop_action_group')
                        break
                    self.__start = True
                    if times < 0:
                        self.__end = False
                        self.__start = True
                        self.stop_action_group = False
                        break
                    self.runAction(actName, lock_servos)
                else:
                    if times < 0:
                        # print('end1')
                        if with_stand:
                            if actName == 'go_forward' or actName == 'go_forward_fast' or actName == 'go_forward_slow':
                                self.runAction('go_forward_end', lock_servos)
                            else:
                                self.runAction('back_end', lock_servos)
                        break
                    if self.__start:
                        self.__start = False
                        self.__end = True
                        # print('start')
                        if actName == 'go_forward' or actName == 'go_forward_slow':
                            self.runAction('go_forward_start', lock_servos)
                            current_status = 'go'
                        elif actName == 'go_forward_fast':
                            self.runAction('go_forward_start_fast', lock_servos)
                            self.current_status = 'go'
                        elif actName == 'back':
                            self.runAction('back_start', lock_servos)
                            self.runAction('back', lock_servos)
                            self.current_status = 'back'
                        elif actName == 'back_fast':
                            self.runAction('back_start', lock_servos)
                            self.runAction('back_fast', lock_servos)
                            self.current_status = 'back'
                    else:
                        self.runAction(actName, lock_servos)
            except BaseException as e:
                print(e)

    def runAction(self, actNum, lock_servos=''):
        '''
        运行动作组，无法发送stop停止信号
        :param actNum: 动作组名字 ， 字符串类型
        :param times:  运行次数
        :return:
        '''

        if actNum is None:
            return "动作组文件名为None"

        actNum = "/root/TonyPiProjectNew/TonyPi/ActionGroups/" + actNum + ".d6a"

        if os.path.exists(actNum) is True:
            if self.runningAction is False:
                self.runningAction = True
                ag = sql.connect(actNum)
                cu = ag.cursor()
                cu.execute("select * from ActionGroup")
                while True:
                    act = cu.fetchone()
                    if self.stop_action is True:
                        self.stop_action = False
                        print('stop')
                        break
                    if act is not None:
                        for i in range(0, len(act) - 2, 1):
                            if str(i + 1) in lock_servos:
                                self.object1.setBusServoPulse(i + 1, lock_servos[str(i + 1)], act[1])
                            else:
                                self.object1.setBusServoPulse(i + 1, act[2 + i], act[1])
                        time.sleep(float(act[1]) / 1000.0)
                    else:  # 运行完才退出
                        break
                self.runningAction = False

                cu.close()
                ag.close()
        else:
            self.runningAction = False
            print("未能找到动作组文件", actNum)

    def runAction_good(self, file_path, lock_servos=''):
        '''
        运行动作组，无法发送stop停止信号
        :param file_path: 动作组文件路径 ， 字符串类型
        :param times:  运行次数
        :return:
        '''

        if file_path is None:
            return "动作组文件路径为None"

        if os.path.exists(file_path) is True:
            if self.runningAction is False:
                self.runningAction = True
                ag = sql.connect(file_path)
                cu = ag.cursor()
                cu.execute("select * from ActionGroup")
                while True:
                    act = cu.fetchone()
                    if self.stop_action is True:
                        self.stop_action = False
                        print('stop')
                        break
                    if act is not None:
                        for i in range(0, len(act) - 2, 1):
                            if str(i + 1) in lock_servos:
                                self.object1.setBusServoPulse(i + 1, lock_servos[str(i + 1)], act[1])
                            else:
                                self.object1.setBusServoPulse(i + 1, act[2 + i], act[1])
                        time.sleep(float(act[1]) / 1000.0)
                    else:  # 运行完才退出
                        break
                self.runningAction = False

                cu.close()
                ag.close()
        else:
            self.runningAction = False
            print("未能找到动作组文件", file_path)


if __name__ == '__main__':

    print("幻尔科技TonyPi扩展板，Bus串行总线舵机控制例程")
    # file_path = "/root/TonyPiProjectNew/TonyPi/ActionGroupsSheng/单手挥手.d6a"
    # file_path = "/root/TonyPiProjectNew/TonyPi/ActionGroups/bow.d6a"
    object1 = BusServoMotion()
    object1.runActionGroup("bow", 1)

    # object1.runActionGroup('stand')  # 参数为动作组的名称，不包含后缀，以字符形式传入
    # object1.runActionGroup('go_forward', times=2, with_stand=True)  # 第二个参数为运行动作次数，默认1, 当为0时表示循环运行， 第三个参数表示最后是否以立正姿态收步
    # object1.runActionGroup('back_fast', 2, True)
    # object1.runActionGroup('1_bow', 1, True)
    #
    # threading.Thread(target=object1.runActionGroup,
    #                  args=('go_forward', 0, True)).start()  # 运行动作函数是阻塞式的，如果要循环运行一段时间后停止，请用线程来开启
    # time.sleep(3)
    # object1.stopActionGroup()  # 前进3秒后停止
