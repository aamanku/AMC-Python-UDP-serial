# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 17:20:45 2020

This programs send Host Read Command to AMC Servo Drive
Serial message is sent over UDP to a target computer which then sends the command to servo Drive

@author: amkulk
"""

import socket
import struct
import time
import crcmod
from binascii import unhexlify

UDP_IP = '192.168.2.111'#host ip
UDP_PORT = 6970

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

def getCommand():
    NumberofBytes='08' #number of bytes in the message, Simulink RTOS requires it in rs232 block
    SOF='A5'    #from manual
    Address='3F'    #factory default
    Control_Byte='01'   #contains no data
    #Refer serial communication manual for below
    Index=input('Enter Index in hex: ')
    Offset=input('Enter Offset in hex: ')
    Data_Word=input('Enter Data_Words: ') #Length of return data (number of 2 Bytes words)
    
    Command_wo_CRC=SOF+Address+Control_Byte+Index+Offset+Data_Word
    Command_wo_CRC_bin=unhexlify(Command_wo_CRC)
    crc16 = crcmod.predefined.Crc('xmodem')     # crc16=crcmod.mkCrcFun(0x11021,0x0000,False,0x0000)
    crc16.update(Command_wo_CRC_bin)
    CRC=crc16.hexdigest()
    Command=NumberofBytes+Command_wo_CRC+CRC
    Command_bin=unhexlify(Command)
    return Command_bin


if __name__=='__main__':
    old_time=time.time()
    while True:
        new_time=time.time()
        if new_time-old_time>0.2:   #wait time from manual
            data=getCommand()
            sock.sendto(data, ('192.168.2.104',6969))#ip of target pc
            print('Sent command: ',data)
            old_time=time.time()