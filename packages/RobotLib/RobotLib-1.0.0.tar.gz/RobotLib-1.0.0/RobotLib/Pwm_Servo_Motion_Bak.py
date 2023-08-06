import time
import pigpio
from Pwm_Servo_Lib import PwmServo


class PwmServoMotion(object):
    pi = pigpio.pi()
    d = [0, 0]

    def __init__(self):
        servo1 = PwmServo(self.pi, 5, deviation=self.d[0], control_speed=True)  # 扩展板上的1
        servo2 = PwmServo(self.pi, 6, deviation=self.d[1], control_speed=True)  # 扩展板上的2
        self.Servos = (servo1, servo2)

    def setPWMServoPulse(self, servo_id, pulse, use_time):
        if servo_id < 1 or servo_id > 2:
            return

        pulse = 2500 if pulse > 2500 else pulse
        pulse = 500 if pulse < 500 else pulse
        use_time = 30000 if use_time > 30000 else use_time
        use_time = 20 if use_time < 20 else use_time

        self.Servos[servo_id - 1].setPosition(pulse, use_time)

        return pulse

    def setDeviation(self, servo_id, dev):
        if servo_id < 1 or servo_id > 2:
            return
        if self.d < -300 or self.d > 300:
            return
        self.Servos[servo_id - 1].setDeviation(dev)


if __name__ == "__main__":

    print("幻尔科技TonyPi扩展板，PWM舵机控制例程")
    object1 = PwmServoMotion()
    while True:
        # 参数：参数1：舵机接口编号; 参数2：位置; 参数3：运行时间
        object1.setPWMServoPulse(2, 1500, 500)  # 2号舵机转到1500位置，用时500ms
        time.sleep(0.5)  # 延时时间和运行时间相同
        object1.setPWMServoPulse(2, 1800, 500)  # 舵机的转动范围0-180度，对应的脉宽为500-2500,即参数2的范围为500-2500
        time.sleep(0.5)
        object1.setPWMServoPulse(2, 1500, 200)
        time.sleep(0.2)
        object1.setPWMServoPulse(2, 1800, 500)
        time.sleep(0.2)

        object1.setPWMServoPulse(1, 1500, 500)
        time.sleep(0.2)
        object1.setPWMServoPulse(1, 1800, 500)
        time.sleep(0.2)
        object1.setPWMServoPulse(1, 1500, 500)
        time.sleep(0.2)
        object1.setPWMServoPulse(1, 1800, 500)
        time.sleep(0.5)
