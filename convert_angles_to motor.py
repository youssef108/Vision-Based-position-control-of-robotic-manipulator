from math import pi
import serial
import cv2 as cv
import sys
import time
stepsPerRevolution = [32800,6800,-6800,20800,-7200];  #microsteps/revolution (using 16ths) from observation, for each motor (int)
joint_status = 0 #int
cur_angle=[0.0,0.0,0.0,0.0,0.0,0.0] #float
joint_step=[0,0,0,0,0,0] #int
prev_angle = [0.0,0.0,0.0,0.0,0.0,0.0] 
init_angle = [0.0,0.0,0.0,0.0,0.0,0.0]
total_steps = [0.0,0.0,0.0,0.0,0.0,0.0]
arm_steps=[0,0,0,0,0,0]
totalPosition=[0,0,0,0,0]
desired=[0,90,90,90]
def cmd_cb(JointPositions):
    # if (count==0):
    #     prev_angle[0] = JointPositions[0]
    #     prev_angle[1] = JointPositions[1]
    #     prev_angle[2] = JointPositions[2]
    #     prev_angle[3] = JointPositions[3]
    #     prev_angle[4] = JointPositions[4]
    #     prev_angle[5] = JointPositions[5]

    #     init_angle[0] = JointPositions[0]
    #     init_angle[1] = JointPositions[1]
    #     init_angle[2] = JointPositions[2]
    #     init_angle[3] = JointPositions[3]
    #     init_angle[4] = JointPositions[4]
    #     init_angle[5] = JointPositions[5]
    arm_steps[0] = (int)((JointPositions[0]-prev_angle[0])*stepsPerRevolution[0]/(360))
    arm_steps[1] = (int)((JointPositions[1]-prev_angle[1])*stepsPerRevolution[1]/(360))
    arm_steps[2] = (int)((JointPositions[2]-prev_angle[2])*stepsPerRevolution[2]/(360))
    arm_steps[3] = (int)((JointPositions[3]-prev_angle[3])*stepsPerRevolution[3]/(360))
    arm_steps[4] = (int)((JointPositions[4]-prev_angle[4])*stepsPerRevolution[4]/(360))


    # if (count!=0):
    prev_angle[0] = JointPositions[0]
    prev_angle[1] = JointPositions[1]
    prev_angle[2] = JointPositions[2]
    prev_angle[3] = JointPositions[3]
    prev_angle[4] = JointPositions[4]

    
    totalPosition[0] += arm_steps[0]
    totalPosition[1] += arm_steps[1]
    totalPosition[2] += arm_steps[2]
    totalPosition[3] += arm_steps[3]
    totalPosition[4] += arm_steps[4]


    return totalPosition
def ArraytoString(Array):
    string= ''
    i=0
    while (i<len(Array)):
        string+=str(Array[i])
        string+=','
        i+=1
    return string    
arduinoData=serial.Serial('com4',115200)
time.sleep(5)
count=0
while True:
    
    time.sleep(1)
    #prev_angle=currentAngle  current angle get from main
    if(prev_angle!=desired  and  count!=0):
        total=cmd_cb(desired)
    if(count)
    count+=1
    print(total)
    cmd=ArraytoString(total)
    cmd=cmd+'\r'
    #print(cmd)
    arduinoData.write(cmd.encode())

    while(arduinoData.inWaiting()==0):
        pass
    data=arduinoData.readline()
    data=str(data,'utf-8')
    data=data.strip('\r\n')
    # data=data.split(",")
    print(data)
    time.sleep(3)
