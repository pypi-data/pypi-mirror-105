#2021年4月13日版
import struct
import threading
import time
import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_tcp as modbus_tcp
import signal
import socket


ROBOT_M8 = 0
ROBOT_R4 = 1
ROBOT_S4 = 2
ROBOT_R6 = 3
def bytesToFloat(float_h, float_l):
    ba = bytearray()
    ba.append(float_h >> 8)
    ba.append(float_h & 0xff)
    ba.append(float_l >> 8)
    ba.append(float_l & 0xff)
    return float(struct.unpack("!f", ba)[0])


def floatToBytes(f):
    bs = struct.pack(">f", f)
    return [(bs[2] << 8)+bs[3], (bs[0] << 8)+bs[1]]


class ZtModTcp():
    RISING = 1
    FALLING = 2
    CHANGE = 3
    id = 0
    TYPE_S = 0
    TYPE_R = 1
    def __init__(self, id, port=502, type = ROBOT_M8):
        self.motor = []
        self.digital_io = []
        self.id = id
        self.type = type
        if self.tcp_server_init(port)==False:
            exit(0)
        self.digital_io_fake_interrupt()
        self.motor_init()

    def tcp_master_init(self, port):
        try:
            self.master = modbus_tcp.TcpMaster(host="127.0.0.1", port=port)
            self.master.set_timeout(1)
        except Exception as e:
            print(e)

    def tcp_server_init(self, port):
        try:
            if self.check_port_conflict(port):
                print("Port %d has been used" % port)
                return False
            self.server = modbus_tcp.TcpServer(
                port=port, address="127.0.0.1", timeout_in_sec=1)
            modbus_tcp.TcpMaster()
            # self.server.set_verbose(True)
            self.server.start()

            self.register_init()
            self.motor_init()
            self.tcp_master_init(port)
            return True
        except Exception as e:
            print(e)
            return False

    def register_init(self):
        # 建立第一个从机
        self.slave = self.server.add_slave(self.id)
        # DI 00-31（32个）	0x寄存器	1024~1055
        self.slave.add_block('A', cst.READ_COILS, 1024, 32)  # 地址0，长度4
        # DO接口	00-31（32个）	0x寄存器	20000~20031
        self.slave.add_block('B', cst.COILS, 20000, 32)

        # FI32接口	00-07（8个）	4x寄存器	1024~1039
        self.slave.add_block('C', cst.READ_HOLDING_REGISTERS, 1024, 16)
        # FO32接口	00-07（8个）	4x寄存器	1040~1055
        self.slave.add_block('D', cst.HOLDING_REGISTERS, 1040, 16)
        # AO MOTO接口	00-07（8个）	4x寄存器	10000~10015
        self.slave.add_block('E', cst.HOLDING_REGISTERS, 10000, 64)
        # just register prevent print error
        self.slave.add_block('F', cst.HOLDING_REGISTERS, 2000, 32)
        self.slave.add_block('G', cst.HOLDING_REGISTERS, 1100, 64)

    def NewR4Robot(self,heightArmBase, lenBigArm, lenSmallArm):
        self.R4.heightArmBase = heightArmBase
        self.R4.lenBigArm = lenBigArm
        self.R4.lenSmallArm = lenSmallArm

    def motor_init(self):
        for __ in range(8):
            motor_config = {"now_pos": 0, "speed": 0,
                            "running_flag": 0, "dst_pos": 0, "status": 0}
            self.motor.append(motor_config)

    def digital_VSR_Read(self, pin):
        if pin < 0 or pin > 31:
            return
        return self.master.execute(self.id, cst.READ_COILS, 1024 + pin, 1)[0]

    def digital_VSR_Write(self, pin, val):
        if pin < 0 or pin > 31:
            return
        self.master.execute(self.id, cst.WRITE_SINGLE_COIL,
                            20000 + pin,  output_value=val)

    # 测试通过
    def Float32_Read(self, pin):
        if pin < 0 or pin > 7:
            return
        data = self.master.execute(
            self.id, cst.READ_HOLDING_REGISTERS, 1024 + pin * 2, 2)
        return bytesToFloat(data[1], data[0])

    def Float32_Write(self, pin, val):
        if pin < 0 or pin > 7:
            return
        self.master.execute(self.id, cst.WRITE_MULTIPLE_REGISTERS,
                            1040 + pin*2, output_value=floatToBytes(val))

    def motor_Float32_Write(self, motor, pos):
        if motor < 0 or motor > 7:
            return
        try:
            self.master.execute(self.id, cst.WRITE_MULTIPLE_REGISTERS,
                                10000 + motor*2, output_value=floatToBytes(pos))
        except Exception as e:
            print(e)

    def motor_run_thread(self, motor):
        run_interval = 0.01
        while True:
            if self.motor[motor]["now_pos"] < self.motor[motor]["dst_pos"]:
                if(self.motor[motor]["now_pos"]+self.motor[motor]["speed"]*run_interval > self.motor[motor]["dst_pos"]):
                    self.motor_Float32_Write(
                        motor, self.motor[motor]["dst_pos"])
                    self.motor[motor]["now_pos"] = self.motor[motor]["dst_pos"]
                else:
                    self.motor_Float32_Write(
                        motor, self.motor[motor]["now_pos"] + self.motor[motor]["speed"]*run_interval)
                    self.motor[motor]["now_pos"] += self.motor[motor]["speed"]*run_interval
                time.sleep(run_interval)
            elif self.motor[motor]["now_pos"] > self.motor[motor]["dst_pos"]:
                if(self.motor[motor]["now_pos"]-self.motor[motor]["speed"]*run_interval < self.motor[motor]["dst_pos"]):
                    self.motor_Float32_Write(
                        motor, self.motor[motor]["dst_pos"])
                    self.motor[motor]["now_pos"] = self.motor[motor]["dst_pos"]
                else:
                    self.motor_Float32_Write(
                        motor, self.motor[motor]["now_pos"] - self.motor[motor]["speed"]*run_interval)
                    self.motor[motor]["now_pos"] -= self.motor[motor]["speed"]*run_interval
                time.sleep(run_interval)
            else:
                break

        self.motor[motor]["status"] = 0

    def Set_ServoPos(self, motor, pos):
        if motor < 0 or motor > 7 or self.motor[motor]["status"]:
            return
        self.motor[motor]["status"] = 1
        self.motor[motor]["dst_pos"] = pos
        threading.Thread(target=self.motor_run_thread, args=(motor,)).start()

    def Get_ServoPos(self, motor):
        if motor < 0 or motor > 7:
            return
        return self.motor[motor]["now_pos"]
        
    def WaitFinish_ServoPos(self, motor):
        if motor < 0 or motor > 7:
            return
        while self.motor[motor]["status"]:
            time.sleep(0.01)
            pass
        

    def digital_io_check(self):
        last_status = self.master.execute(self.id, cst.READ_COILS, 1024, 32)
        while True:
            try:
                #         for 循环轮询每一个IO的状态
                now_status = self.master.execute(
                    self.id, cst.READ_COILS, 1024, 32)
                count = -1
                for status in now_status:
                    count = count + 1
                    if self.digital_io[count]["enable"] == 0:
                        continue
                    if status != last_status[count] and self.digital_io[count]["irq_mode"] == self.CHANGE and self.digital_io[count]["change_func"] != 0:
                        self.digital_io[count]["change_func"]()
                    if status < last_status[count]:
                        if self.digital_io[count]["irq_mode"] == self.FALLING and self.digital_io[count]["irq_falling_func"] != 0:
                            self.digital_io[count]["irq_falling_func"]()
                    elif status > last_status[count]:
                        if self.digital_io[count]["irq_mode"] == self.RISING and self.digital_io[count]["irq_rising_func"] != 0:
                            self.digital_io[count]["irq_rising_func"]()
                last_status = now_status
            except Exception as e:
                print(e)

    def check_port_conflict(self, port):
        ret = False
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', port))
        if result == 0:
            ret = True
        else:
            ret = False
        sock.close()
        return ret

    def digital_VSR_AttachInterrupt(self, pin, func, mode):
        if pin < 0 or pin > 31:
            return
        if mode != self.FALLING and mode != self.RISING and mode != self.CHANGE:
            return
        self.digital_io[pin]["irq_mode"] = mode
        if mode == self.RISING:
            self.digital_io[pin]["irq_rising_func"] = func
        elif mode == self.FALLING:
            self.digital_io[pin]["irq_falling_func"] = func
        elif mode == self.CHANGE:
            self.digital_io[pin]["change_func"] = func
        self.digital_io[pin]["enable"] = 1

    def digital_io_fake_interrupt(self):
        self.digital_io = []
        for __ in range(32):
            data = {"irq_mode": 0, "irq_rising_func": 0,
                    "irq_falling_func": 0, "enable": 0, "change_func": 0}
            self.digital_io.append(data)
        threading.Thread(target=self.digital_io_check).start()

    def digital_VSR_InterruptDisable(self, pin):
        if pin < 0 or pin > 31:
            return
        self.digital_io[pin]["enable"] = 0

    def digital_VSR_InterruptEnable(self, pin):
        if pin < 0 or pin > 31:
            return
        self.digital_io[pin]["enable"] = 1

    def Set_ServoSpeed(self, motor, speed):
        if motor < 0 or motor > 7:
            return
        self.motor[motor]["speed"] = speed
    
    def Set_R4Speed(self, speed):
        self.motor[0]["speed"] = speed
        self.motor[1]["speed"] = speed
        self.motor[2]["speed"] = speed
        self.motor[3]["speed"] = speed
        self.motor[4]["speed"] = speed
    
    def Set_ScaraSpeed(self, speed):
        self.motor[0]["speed"] = speed
        self.motor[1]["speed"] = speed
        self.motor[2]["speed"] = speed
        self.motor[3]["speed"] = speed
        self.motor[4]["speed"] = speed
    
    def Set_R6Speed(self, speed):
        self.motor[0]["speed"] = speed
        self.motor[1]["speed"] = speed
        self.motor[2]["speed"] = speed
        self.motor[3]["speed"] = speed
        self.motor[4]["speed"] = speed
        self.motor[5]["speed"] = speed
        self.motor[6]["speed"] = speed

    def Get_R4Pos(self, motor):
        if motor < 0 or motor > 3:
            return
        return self.motor[motor]["now_pos"]
    
    def Get_R4ServoPos(self, motor):
        if motor < 0 or motor > 1:
            return
        return self.motor[motor + 4]["now_pos"]

    def Get_ScaraPos(self, motor):
        if motor < 0 or motor > 3:
            return
        return self.motor[motor]["now_pos"]
    
    def Get_ScaraServoPos(self, motor):
        if motor < 0 or motor > 1:
            return
        return self.motor[motor + 4]["now_pos"]
    
    def Get_R6Pos(self, motor):
        if motor < 0 or motor > 5:
            return
        return self.motor[motor]["now_pos"]
    
    def Get_R6ServoPos(self, motor):
        if motor < 0 or motor > 1:
            return
        return self.motor[motor + 6]["now_pos"]

    def Set_R4SerialPos(self, motor, pos):
        if motor < 0 or motor > 3 or self.motor[motor]["status"]:
            return
        self.Set_ServoPos(motor,pos)

    def Set_R4Pos(self, pos1, pos2, pos3, pos4):
        self.Set_ServoPos(0, pos1)
        self.Set_ServoPos(1, pos2)
        self.Set_ServoPos(2, pos3)
        self.Set_ServoPos(3, pos4)

    def Set_R4ServoPos(self, motor, pos):
        if motor < 0 or motor > 1 or self.motor[motor + 4]["status"]:
            return
        self.Set_ServoPos(motor + 4,pos)
    
    def Set_ScaraSerialPos(self, motor, pos):
        if motor < 0 or motor > 3 or self.motor[motor]["status"]:
            return
        self.Set_ServoPos(motor,pos)
    
    def Set_ScaraPos(self, pos1, pos2, pos3, pos4):
        self.Set_ServoPos(0, pos1)
        self.Set_ServoPos(1, pos2)
        self.Set_ServoPos(2, pos3)
        self.Set_ServoPos(3, pos4)

    def Set_ScaraServoPos(self, motor, pos):
        if motor < 0 or motor > 1 or self.motor[motor + 4]["status"]:
            return
        self.Set_ServoPos(motor + 4,pos)

    def Set_R6SerialPos(self, motor, pos):
        if motor < 0 or motor > 5 or self.motor[motor]["status"]:
            return
        self.Set_ServoPos(motor,pos)
    
    def Set_R6Pos(self, pos1, pos2, pos3, pos4, pos5, pos6):
        self.Set_ServoPos(0, pos1)
        self.Set_ServoPos(1, pos2)
        self.Set_ServoPos(2, pos3)
        self.Set_ServoPos(3, pos4)
        self.Set_ServoPos(4, pos5)
        self.Set_ServoPos(5, pos6)

    def Set_R6ServoPos(self, motor, pos):
        if motor < 0 or motor > 1 or self.motor[motor + 6]["status"]:
            return
        self.Set_ServoPos(motor + 6,pos)

    def WaitFinish_R4(self):
        self.WaitFinish_ServoPos(0)
        self.WaitFinish_ServoPos(1)
        self.WaitFinish_ServoPos(2)
        self.WaitFinish_ServoPos(3)

    def WaitFinish_R4ServoPos(self):
        self.WaitFinish_ServoPos(4)
    
    def WaitFinish_Scara(self):
        self.WaitFinish_ServoPos(0)
        self.WaitFinish_ServoPos(1)
        self.WaitFinish_ServoPos(2)
        self.WaitFinish_ServoPos(3)
    
    def WaitFinish_ScaraServoPos(self):
        self.WaitFinish_ServoPos(4)

    def WaitFinish_R6(self):
        self.WaitFinish_ServoPos(0)
        self.WaitFinish_ServoPos(1)
        self.WaitFinish_ServoPos(2)
        self.WaitFinish_ServoPos(3)
        self.WaitFinish_ServoPos(4)
        self.WaitFinish_ServoPos(5)
    
    def WaitFinish_R6ServoPos(self):
        self.WaitFinish_ServoPos(6)

    def stop(self):
        self.server.stop()
