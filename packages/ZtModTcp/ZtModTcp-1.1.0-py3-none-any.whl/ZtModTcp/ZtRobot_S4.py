import os
import json
import struct
import threading
import time
import signal
import math

M_PI = 3.14159265358979323846
M_PI_2 = 1.57079632679489661923

class ZtRobot_S4():
    def __init__(self, info = "ROBOT_S4.json"):
        file = open(info) 
        fileJson = json.load(file)
        self.lenBigArm = fileJson['lenBigArm']
        self.lenSmallArm = fileJson['lenSmallArm']
        self.heightDeviation = fileJson['heightDeviation']
        self.squareBigSubSmallArm = self.lenBigArm * self.lenBigArm + self.lenSmallArm * self.lenSmallArm
        
        self.RAD2ANG = M_PI/180.0
    # 正解函数，根据角度求坐标
    def Joint2Descartes(self, coorJoint):
        coorDescartes = [0,0,0,0,0,0]

        coorJoint[0] = coorJoint[0] * self.RAD2ANG
        coorJoint[1] = coorJoint[1] * self.RAD2ANG
        coorJoint[2] = coorJoint[2]
        coorJoint[3] = coorJoint[3] * self.RAD2ANG
        coorJoint[4] = coorJoint[4] * self.RAD2ANG
        coorJoint[5] = coorJoint[5] * self.RAD2ANG
        
        tempSinT1 = math.sin(coorJoint[0])
        tempCosT1 = math.cos(coorJoint[0])

        tempSinT1T2 = math.sin(coorJoint[0] + coorJoint[1])
        tempCosT1T2 = math.cos(coorJoint[0] + coorJoint[1])

        coorDescartes[0] = self.lenBigArm * tempCosT1 + self.lenSmallArm * tempCosT1T2
        coorDescartes[1] = self.lenBigArm * tempSinT1 + self.lenSmallArm * tempSinT1T2
        coorDescartes[2] = self.heightDeviation + coorJoint[2]
        coorDescartes[3] = coorJoint[0] + coorJoint[1] + coorJoint[3]
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

        tempR = coorDescartes[0] * coorDescartes[0] + coorDescartes[1] * coorDescartes[1]
        tempCosT2 = (tempR - self.squareBigSubSmallArm) / (2.0 * self.lenBigArm * self.lenSmallArm)
        tempSinT2 = math.sqrt(1.0 - tempCosT2 * tempCosT2)


        coorJoint[0] = math.atan2(coorDescartes[1], coorDescartes[0]) - math.atan2((self.lenSmallArm * tempSinT2), (self.lenBigArm + self.lenSmallArm * tempCosT2))
        coorJoint[1] = math.atan2(tempSinT2, tempCosT2)
        coorJoint[2] = coorDescartes[2] - self.heightDeviation
        coorJoint[3] = coorDescartes[3] - coorJoint[0] - coorJoint[1]
        coorJoint[4] = 0
        coorJoint[5] = 0

        coorJoint[0] = coorJoint[0] / self.RAD2ANG
        coorJoint[1] = coorJoint[1] / self.RAD2ANG
        coorJoint[2] = coorJoint[2]
        coorJoint[3] = coorJoint[3] / self.RAD2ANG
        coorJoint[4] = coorJoint[4] / self.RAD2ANG
        coorJoint[5] = coorJoint[5] / self.RAD2ANG
        return coorJoint
