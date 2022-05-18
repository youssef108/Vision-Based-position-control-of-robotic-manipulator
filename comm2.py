#Arduino forum 2020 - https://forum.arduino.cc/index.php?topic=714968

import serial

import sys
import time
arduinoData=serial.Serial('com4',115200)
time.sleep(5)
while True:
    
    cmd="11111,200,3555,4,5000,"
    cmd=cmd+'\r'
    arduinoData.write(cmd.encode())

    while(arduinoData.inWaiting()==0):
        pass
    data=arduinoData.readline()
    data=str(data,'utf-8')
    data=data.strip('\r\n')
    # data=data.split(",")
    print(data)