# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 13:07:44 2020

@author: amkulk
"""

import socket
import struct

buffer_size=1#8 for double
data_type='B' #'d' for double
UDP_IP = '192.168.2.111'#host ip
UDP_PORT = 9696

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

while True:
    raw, addr = sock.recvfrom(10240)
    print(raw)

    Length_Reply=raw[0]
    try:
        Loc_SOF=raw.index(165)  #A5
        Len_Data=raw[Loc_SOF+5] #read manual
        
        Data=raw[Loc_SOF+8:Loc_SOF+8+Len_Data*2]
        print(Data)
        print('h')
    except:
        print('Invalid Message')
sock.close()

