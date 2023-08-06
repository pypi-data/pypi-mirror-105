import os
import json
import struct
import threading
import time
import signal
import math

M_PI = 3.14159265358979323846
M_PI_2 = 1.57079632679489661923

class ZtRobot_R4():
    def __init__(self, info = "ROBOT_R4.json"):
        file = open(info) 
        fileJson = json.load(file)
        self.heightArmBase = fileJson['heightArmBase']
        self.lenBigArm = fileJson['lenBigArm']
        self.lenSmallArm = fileJson['lenSmallArm']
        self.lenDeviation = fileJson['lenDeviation']
        self.heightDeviation = fileJson['heightDeviation']
        self.squareBigSubSmallArm = self.lenBigArm * self.lenBigArm - self.lenSmallArm * self.lenSmallArm
        
        self.RAD2ANG = M_PI/180.0
    # 正解函数，根据角度求坐标
    def Joint2Descartes(self, coorJoint):
        coorDescartes = [0,0,0,0,0,0]

        coorJoint[0] = coorJoint[0] * self.RAD2ANG
        coorJoint[1] = coorJoint[1] * self.RAD2ANG
        coorJoint[2] = coorJoint[2] * self.RAD2ANG
        coorJoint[3] = coorJoint[3] * self.RAD2ANG
        coorJoint[4] = coorJoint[4] * self.RAD2ANG
        coorJoint[5] = coorJoint[5] * self.RAD2ANG
        # 计算中间量减小计算时间
        # 正反三角函数
        tempSinT1 = math.sin(coorJoint[0])
        tempCosT1 = math.cos(coorJoint[0])

        tempSinT2 = math.sin(-(coorJoint[1]))
        tempCosT2 = math.cos(-(coorJoint[1]))

        tempSinT3 = math.sin(-(coorJoint[2]))
        tempCosT3 = math.cos(-(coorJoint[2]))

        tempSinT2T3 = math.sin(-(coorJoint[1]) +(-coorJoint[2]))
        tempCosT2T3 = math.cos(-(coorJoint[1]) + (-coorJoint[2]))

        coorDescartes[3] = coorJoint[0] + coorJoint[3]

        tempTp = coorDescartes[3]
        tempSinTp = math.sin(tempTp)
        tempCosTp = math.cos(tempTp)

        # 先求出工具旋转轴（第四轴）执行末端到原点的XOY平面投影到原点的距离
        tempR = self.lenBigArm * tempSinT2 + self.lenSmallArm * tempCosT2T3 + self.lenDeviation
        # 先求出工具旋转轴（第四轴）执行末端到原点的XOY平面的高度
        tempZ = self.lenBigArm * tempCosT2 - self.lenSmallArm * tempSinT2T3 + self.heightDeviation

        # 计算笛卡尔坐标
        coorDescartes[0] = tempR * tempCosT1
        coorDescartes[1] = tempR * tempSinT1
        coorDescartes[2] = tempZ +  self.heightArmBase
        coorDescartes[4] = 0
        coorDescartes[5] = 0

        coorDescartes[3] = coorDescartes[3] / self.RAD2ANG
        return coorDescartes

    # 反解函数，根据坐标求角度
    def Descartes2Joint(self, coorDescartes):
        coorJoint = [0,0,0,0,0,0]

        coorDescartes[3] = coorDescartes[3] * self.RAD2ANG
        coorDescartes[4] = coorDescartes[4] * self.RAD2ANG
        coorDescartes[5] = coorDescartes[5] * self.RAD2ANG

        # 先求出工具旋转轴（第四轴）执行末端到原点的XOY平面的XY值
        tempX = coorDescartes[0]
        tempY = coorDescartes[1]

        # 求出空间坐标第三轴（小臂）末端到原点的高度和半径
        tempR = math.sqrt(tempX*tempX + tempY * tempY) - self.lenDeviation
        tempZ = coorDescartes[2] - self.heightDeviation - self.heightArmBase

        # 需要重复使用的变量，方便后续带入计算
        tempSquareRZ = tempR * tempR + tempZ * tempZ
        temp2SqrtSquareRZ = 2.0 * math.sqrt(tempSquareRZ)
        tempAtan2ZR = math.atan2(tempZ, tempR)

        tempT2ASinVal = (tempSquareRZ + self.squareBigSubSmallArm) / (self.lenBigArm * temp2SqrtSquareRZ)
        tempT3ASinVal = (self.squareBigSubSmallArm - tempSquareRZ) / (self.lenSmallArm * temp2SqrtSquareRZ)

        tempT2X = math.sqrt(1.0 - tempT2ASinVal * tempT2ASinVal)
        tempT3X = math.sqrt(1.0 - tempT3ASinVal * tempT3ASinVal)

        coorJoint[0] = math.atan2(tempY, tempX)
        coorJoint[1] = math.atan2(tempT2ASinVal, tempT2X) - tempAtan2ZR
        coorJoint[2] = math.atan2(tempT3ASinVal, tempT3X) + (M_PI_2 - tempAtan2ZR)
        coorJoint[3] = coorDescartes[3] - coorJoint[0]
        coorJoint[4] = 0
        coorJoint[5] = 0
        coorJoint[1] = -coorJoint[1]
        coorJoint[2] = (-coorJoint[2]) - coorJoint[1]

        coorJoint[0] = coorJoint[0] / self.RAD2ANG
        coorJoint[1] = coorJoint[1] / self.RAD2ANG
        coorJoint[2] = coorJoint[2] / self.RAD2ANG
        coorJoint[3] = coorJoint[3] / self.RAD2ANG
        coorJoint[4] = coorJoint[4] / self.RAD2ANG
        coorJoint[5] = coorJoint[5] / self.RAD2ANG
        return coorJoint

