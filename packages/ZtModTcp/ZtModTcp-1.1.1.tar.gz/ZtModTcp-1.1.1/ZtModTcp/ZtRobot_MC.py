import struct
import threading
import time
import signal
import math

# 直线插补与角速度的比例值
ROBOT_MC_LINE_RATE = 60
# 直线单位线段长度
ROBOT_MC_LINE_UNIT = 50

class ZtRobot_MC():
    def __init__(self, nums, run_interval):
        self.pos= []
        self.target = []
        self.speed = 5
        self.pos_array = []
        self.nums = nums
        self.run_interval = run_interval

    # 最多8轴点到点插补 pos：当前坐标，target：目标位置，speed，速度
    def MC_Point(self, pos, target, speed):
        # 存储插补后的点,改数组为一个2维数组，存储8个电机的值
        pos_array = []
        for __ in range(self.nums):
            pos_array.append([])
        # 电机序号和电机运动距离的最大差值
        motorSerial = 0
        motorTemp = 0
        # 最大运动角度的电机序号
        motorTempSerial = 0
        # 最大运动角度最终的差值数组数量
        motorAddNums = 0
        # 联动轴的插补数据序号和每次插补的单位数
        motorAddNumSerial = 0
        motorAddSerialPos = 0
        while motorSerial < self.nums :
            if motorTemp < abs(target[motorSerial] - pos[motorSerial]):
                motorTemp = abs(target[motorSerial] - pos[motorSerial])
                motorTempSerial = motorSerial
            motorSerial += 1
        run_interval = self.run_interval
        # 第一个点位当前点
        pos_array[motorTempSerial].append(pos[motorTempSerial])
        # 对运动最大的轴进行插补
        while True: 
            if pos_array[motorTempSerial][motorAddNums] < target[motorTempSerial]:
                if pos_array[motorTempSerial][motorAddNums] + speed * run_interval > target[motorTempSerial]:
                    pos_array[motorTempSerial].append(target[motorTempSerial])
                    motorAddNums += 1
                else:
                    pos_array[motorTempSerial].append(pos_array[motorTempSerial][motorAddNums] + speed * run_interval)
                    motorAddNums += 1
            elif pos_array[motorTempSerial][motorAddNums] > target[motorTempSerial]:
                if pos_array[motorTempSerial][motorAddNums] - speed * run_interval < target[motorTempSerial]:
                    pos_array[motorTempSerial].append(target[motorTempSerial])
                    motorAddNums += 1
                else:
                    pos_array[motorTempSerial].append(pos_array[motorTempSerial][motorAddNums] - speed * run_interval)
                    motorAddNums += 1
            else:
                break 
        # 对其他所有的轴进行插补
        motorSerial = 0
        while motorSerial < self.nums:
            if motorSerial != motorTempSerial:
                motorAddNumSerial = 0
                pos_array[motorSerial].append(pos[motorSerial])
                if motorAddNums == 0:
                    continue
                motorAddSerialPos = abs(target[motorSerial] - pos[motorSerial]) / motorAddNums
                while motorAddNumSerial < motorAddNums:
                    if pos_array[motorSerial][motorAddNumSerial] < target[motorSerial]:
                        if pos_array[motorSerial][motorAddNumSerial] + motorAddSerialPos > target[motorSerial]:
                            pos_array[motorSerial].append(target[motorSerial])
                            motorAddNumSerial += 1
                        else:
                            pos_array[motorSerial].append(pos_array[motorSerial][motorAddNumSerial] + motorAddSerialPos)
                            motorAddNumSerial += 1
                    elif pos_array[motorSerial][motorAddNumSerial] > target[motorSerial]:
                        if pos_array[motorSerial][motorAddNumSerial] - motorAddSerialPos < target[motorSerial]:
                            pos_array[motorSerial].append(target[motorSerial])
                            motorAddNumSerial += 1
                        else:
                            pos_array[motorSerial].append(pos_array[motorSerial][motorAddNumSerial] - motorAddSerialPos)
                            motorAddNumSerial += 1
                    else:
                        pos_array[motorSerial].append(target[motorSerial])
                        motorAddNumSerial += 1
            motorSerial += 1
        # 删除插补的第一个点，即起始点
        motorSerial = 0
        while motorSerial < self.nums:
            pos_array[motorSerial].pop(0)
            motorSerial += 1 
        return pos_array

    # XYZ三轴坐标系的直线插补
    def MC_Line_R3(self, pos, target, speed):
        # 存储插补后的点,改数组为一个2维数组，存储XYZ三个坐标
        pos_array = []
        for __ in range(self.nums):
            pos_array.append([])
        # 计算差值
        pos_unit = [0,0,0]
        for i in range(3):
            pos_unit[i] = target[i] - pos[i]
        #计算线段长度
        lenLine = math.sqrt(pos_unit[0] * pos_unit[0] + pos_unit[1] * pos_unit[1] + pos_unit[2] * pos_unit[2])
        lenNums = 0
        if (lenLine % ROBOT_MC_LINE_UNIT) == 0:
            lenNums = lenLine // ROBOT_MC_LINE_UNIT
        else:
            lenNums = lenLine // ROBOT_MC_LINE_UNIT + 1
        if lenNums == 0:
            return pos_array
        # 计算单元长度
        for i in range(3):
            pos_unit[i] = pos_unit[i] / lenNums
        # 对前面3个轴进行直线插补
        motorSerial = 0
        while motorSerial < 3:
            motorAddNumSerial = 0
            motorAddSerialPos = abs(pos_unit[motorSerial])
            pos_array[motorSerial].append(pos[motorSerial])
            while motorAddNumSerial < lenNums:
                if pos_array[motorSerial][motorAddNumSerial] < target[motorSerial]:
                    if pos_array[motorSerial][motorAddNumSerial] + motorAddSerialPos > target[motorSerial]:
                        pos_array[motorSerial].append(target[motorSerial])
                        motorAddNumSerial += 1
                    else:
                        pos_array[motorSerial].append(pos_array[motorSerial][motorAddNumSerial] + motorAddSerialPos)
                        motorAddNumSerial += 1
                elif pos_array[motorSerial][motorAddNumSerial] > target[motorSerial]:
                    if pos_array[motorSerial][motorAddNumSerial] - motorAddSerialPos < target[motorSerial]:
                        pos_array[motorSerial].append(target[motorSerial])
                        motorAddNumSerial += 1
                    else:
                        pos_array[motorSerial].append(pos_array[motorSerial][motorAddNumSerial] - motorAddSerialPos)
                        motorAddNumSerial += 1
                else:
                    pos_array[motorSerial].append(target[motorSerial])
                    motorAddNumSerial += 1
            motorSerial += 1
        # 对额外的几个轴进行PTP插补
        while motorSerial < self.nums:
            motorAddNumSerial = 0
            motorAddSerialPos = abs(target[motorSerial] - pos[motorSerial]) / lenNums
            pos_array[motorSerial].append(pos[motorSerial])
            while motorAddNumSerial < lenNums:
                if pos_array[motorSerial][motorAddNumSerial] < target[motorSerial]:
                    if pos_array[motorSerial][motorAddNumSerial] + motorAddSerialPos > target[motorSerial]:
                        pos_array[motorSerial].append(target[motorSerial])
                        motorAddNumSerial += 1
                    else:
                        pos_array[motorSerial].append(pos_array[motorSerial][motorAddNumSerial] + motorAddSerialPos)
                        motorAddNumSerial += 1
                elif pos_array[motorSerial][motorAddNumSerial] > target[motorSerial]:
                    if pos_array[motorSerial][motorAddNumSerial] - motorAddSerialPos < target[motorSerial]:
                        pos_array[motorSerial].append(target[motorSerial])
                        motorAddNumSerial += 1
                    else:
                        pos_array[motorSerial].append(pos_array[motorSerial][motorAddNumSerial] - motorAddSerialPos)
                        motorAddNumSerial += 1
                else:
                    pos_array[motorSerial].append(target[motorSerial])
                    motorAddNumSerial += 1
            motorSerial += 1
        # 删除插补的第一个点，即起始点
        motorSerial = 0
        while motorSerial < self.nums:
            pos_array[motorSerial].pop(0)
            motorSerial += 1 
        return pos_array
        
