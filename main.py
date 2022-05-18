import sys
from turtle import back
import cv2
import numpy as np
import time
# Functions
import HSV_filter as hsv
from display import display
import shape_recognition as shape
import triangulation as tri
import Kinematics
import collections
import serial


#display
# Open both cameras
counter=0
def averaging_filter(array):
    sum=0
    for i in range(0, len(array)):
        sum += array[i]
    return sum/6
def compareArray(current,prev):
    flag= True
    i=0
    while(i<5):
        if(abs(current[i]-prev[i])<1.5):
            flag=False
            return flag
    return flag       
def ArraytoString(Array):
    string= ''
    i=0
    while (i<len(Array)):
        string+=str(Array[i])
        string+=','
        i+=1
    return string  
# communication and control 
stepsPerRevolution = [32800,-6800,6800,20800,-7200];  #microsteps/revolution (using 16ths) from observation, for each motor (int)
joint_status = 0 #int
cur_angle=[0.0,0.0,0.0,0.0,0.0,0.0] #float
joint_step=[0,0,0,0,0,0] #int
prev_angle = [0.0,0.0,0.0,0.0,0.0] 
init_angle = [0.0,0.0,0.0,0.0,0.0,0.0]
total_steps = [0.0,0.0,0.0,0.0,0.0,0.0]
arm_steps=[0,0,0,0,0,0]
totalPosition=[0,0,0,0,0]
desired=[0,70,0,0]

cap_right = cv2.VideoCapture(2, cv2.CAP_DSHOW)                    
cap_left =  cv2.VideoCapture(1, cv2.CAP_DSHOW)
cap_right.set(3,800)
cap_right.set(4,720)
cap_left.set(3,800)
cap_left.set(4,720)
frame_rate = 120    #Camera frame rate (maximum at 120 fps)

B = 9.28874               #Distance between the cameras [cm]
f = 4              #Camera lense's focal length [mm]
alpha = 56.6        #Camera field of view in the horisontal plane [degrees]
cv_file = cv2.FileStorage()
cv_file.open('stereoMap.xml', cv2.FileStorage_READ)

stereoMapL_x = cv_file.getNode('stereoMapL_x').mat()
stereoMapL_y = cv_file.getNode('stereoMapL_y').mat()
stereoMapR_x = cv_file.getNode('stereoMapR_x').mat()
stereoMapR_y = cv_file.getNode('stereoMapR_y').mat()
#base coordinates
x=0
y=0
z=0
first= True
#Initial values
count = -1
bufferxj1=[0,0,0,0,0,0]
bufferxj1=collections.deque(bufferxj1)
bufferyj1=[0,0,0,0,0,0]
bufferyj1=collections.deque(bufferyj1)
bufferzj1=[0,0,0,0,0,0]
bufferzj1=collections.deque(bufferzj1)
bufferxj2=[0,0,0,0,0,0]
bufferxj2=collections.deque(bufferxj2)
bufferyj2=[0,0,0,0,0,0]
bufferyj2=collections.deque(bufferyj2)
bufferzj2=[0,0,0,0,0,0]
bufferzj2=collections.deque(bufferzj2)
bufferxj3=[0,0,0,0,0,0]
bufferxj3=collections.deque(bufferxj3)
bufferyj3=[0,0,0,0,0,0]
bufferyj3=collections.deque(bufferyj3)
bufferzj3=[0,0,0,0,0,0]
bufferzj3=collections.deque(bufferzj3)
bufferxj4=[0,0,0,0,0,0]
bufferxj4=collections.deque(bufferxj4)
bufferyj4=[0,0,0,0,0,0]
bufferyj4=collections.deque(bufferyj4)
bufferzj4=[0,0,0,0,0,0]
bufferzj4=collections.deque(bufferzj4)
#robot control values
def cmd_cb(JointPositions,q1,q2,q3,q4):
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
    arm_steps[2] = (int)((JointPositions[1]-prev_angle[2])*stepsPerRevolution[2]/(360))
    arm_steps[3] = (int)((JointPositions[2]-prev_angle[3])*stepsPerRevolution[3]/(360))
    arm_steps[4] = (int)((JointPositions[3]-prev_angle[4])*stepsPerRevolution[4]/(360))


    # if (count!=0):
    # prev_angle[0] = 0
    # prev_angle[1] = q2
    # prev_angle[2] = q2
    # prev_angle[3] = q3
    # prev_angle[4] = q4

    
    totalPosition[0] += arm_steps[0]
    totalPosition[1] += arm_steps[1]
    totalPosition[2] += arm_steps[2]
    totalPosition[3] += arm_steps[3]
    totalPosition[4] += arm_steps[4]


    return totalPosition

# desiredAngles=[0,40,40,70,90]#desired angles for steppers to go
arduinoData=serial.Serial('com4',115200)
time.sleep(5)
prevtime=time.time()

while(True):
    count += 1

    ret_right, frame_right = cap_right.read()
    ret_left, frame_left = cap_left.read()

################## CALIBRATION #########################################################

    frame_right = cv2.remap(frame_right, stereoMapR_x, stereoMapR_y, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
    frame_left = cv2.remap(frame_left, stereoMapL_x, stereoMapL_y, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)

########################################################################################

    # If cannot catch any frame, break
    if ret_right==False or ret_left==False:                    
        break

    else:
        # APPLYING HSV-FILTER:
        #joint 1
        mask_right_y = hsv.add_HSV_filter(frame_right, 'y')
        mask_left_y = hsv.add_HSV_filter(frame_left, 'y')
        circles_right_y = shape.find_circles(frame_right, mask_right_y)
        circles_left_y  = shape.find_circles(frame_left, mask_left_y)
        #joint 2
        mask_right_b = hsv.add_HSV_filter(frame_right, 'b')
        mask_left_b = hsv.add_HSV_filter(frame_left, 'b')
        circles_right_b = shape.find_circles(frame_right, mask_right_b)
        circles_left_b  = shape.find_circles(frame_left, mask_left_b)
        #joint 3
        mask_right_g = hsv.add_HSV_filter(frame_right, 'g')
        mask_left_g = hsv.add_HSV_filter(frame_left, 'g')
        circles_right_g = shape.find_circles(frame_right, mask_right_g)
        circles_left_g  = shape.find_circles(frame_left, mask_left_g)
        #end effector
        mask_right_r = hsv.add_HSV_filter(frame_right, 'r')
        mask_left_r = hsv.add_HSV_filter(frame_left, 'r')
        circles_right_r = shape.find_circles(frame_right, mask_right_r)
        circles_left_r  = shape.find_circles(frame_left, mask_left_r)
        #drawing lines between joints
        
        if(circles_left_b != None and circles_left_y!=None and circles_right_y != None and circles_right_b!=None and circles_left_g!=None and circles_right_g!= None):
            #line joint 1 to 2
            x1l = circles_left_y[0]
            y1l = circles_left_y[1]
            x2l=circles_left_b[0]
            y2l= circles_left_b[1]
            cv2.line(frame_left,(x1l,y1l),(x2l,y2l),(0,255,255),3)
            x1r=circles_right_y[0]
            y1r=circles_right_y[1]
            x2r= circles_right_b[0]
            y2r=circles_right_b[1]
            cv2.line(frame_right,(x1r,y1r),(x2r,y2r),(0,255,255),3)
            #line joint 2 to 3
            x3l=circles_left_g[0]
            y3l= circles_left_g[1]
            cv2.line(frame_left,(x2l,y2l),(x3l,y3l),(0,255,255),3)
            x3r= circles_right_g[0]
            y3r=circles_right_g[1]
            cv2.line(frame_right,(x2r,y2r),(x3r,y3r),(0,255,255),3)
        #cv2.line(frame_right,(circles_left_b[0],circles_left_b[1]),(circles_left_r[0],circles_left_r[1]),(0,255,255),2)
        # Result-frames after applying HSV-filter mask
        # res_right = cv2.bitwise_and(frame_right, frame_right, mask=mask_right)
        # res_left = cv2.bitwise_and(frame_left, frame_left, mask=mask_left) 
        
        ################## CALCULATING BALL DEPTH #########################################################

        # If no ball can be caught in one camera show text "TRACKING LOST"
        if np.all(circles_right_y) == None or np.all(circles_left_y) == None :
            cv2.putText(frame_right, "TRACKING LOST", (75,50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255),2)
            cv2.putText(frame_left, "TRACKING LOST", (75,50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255),2)

        else:
            # Function to calculate depth of object. Outputs vector of all depths in case of several balls.
            # All formulas used to find depth is in video presentaion
            zj1 ,xj1, yj1 = tri.find_depth(circles_right_y, circles_left_y, frame_right, frame_left, B, f, alpha)
            zj2 ,xj2,yj2 = tri.find_depth(circles_right_b, circles_left_b, frame_right, frame_left, B, f, alpha)
            zj3 ,xj3,yj3 = tri.find_depth(circles_right_g, circles_left_g, frame_right, frame_left, B, f, alpha)
            zj4 ,xj4,yj4 = tri.find_depth(circles_right_r, circles_left_r, frame_right, frame_left, B, f, alpha)
            #applying filter
            if(counter>6):
                bufferxj1.pop()
                bufferxj1.appendleft(xj1)
                bufferxj2.pop()
                bufferxj2.appendleft(xj2)
                bufferxj3.pop()
                bufferxj3.appendleft(xj3)
                bufferxj4.pop()
                bufferxj4.appendleft(xj4)
                bufferyj1.pop()
                bufferyj1.appendleft(yj1)
                bufferyj2.pop()
                bufferyj2.appendleft(yj2)
                bufferyj3.pop()
                bufferyj3.appendleft(yj3)
                bufferyj4.pop()
                bufferyj4.appendleft(yj4)
                bufferzj1.pop()
                bufferzj1.appendleft(zj1)
                bufferzj2.pop()
                bufferzj2.appendleft(zj2)
                bufferzj3.pop()
                bufferzj3.appendleft(zj3)
                bufferzj4.pop()
                bufferzj4.appendleft(zj4)
                xj1=averaging_filter(bufferxj1)
                xj2=averaging_filter(bufferxj2)
                xj3=averaging_filter(bufferxj3)
                xj4=averaging_filter(bufferxj4)
                yj1=averaging_filter(bufferyj1)
                yj2=averaging_filter(bufferyj2)
                yj3=averaging_filter(bufferyj3)
                yj4=averaging_filter(bufferyj4)
                zj1=averaging_filter(bufferzj1)
                zj2=averaging_filter(bufferzj2)
                zj3=averaging_filter(bufferzj3)
                zj4=averaging_filter(bufferzj4)

            counter=counter+1        
            if(first):
                x=xj1
                y=yj1
                z=zj1-18
                first=False 
            xj1,yj1,zj1,xj2,yj2,zj2,xj3,yj3,zj3,xj4,yj4,zj4=Kinematics.relateCoordinates(x,y,z,xj1,yj1,zj1,xj2,yj2,zj2,xj3,yj3,zj3,xj4,yj4,zj4)   
           
            q1,q2,q3,q4=Kinematics.getAngles(xj1,yj1,zj1,xj2,yj2,zj2,xj3,yj3,zj3,xj4,yj4,zj4)
            prev_angle=[q1,q2,q2,q3,q4]
            # display(background,xj1,yj1,zj1,xj2,yj2,zj2,xj3,yj3,zj3,xj4,yj4,zj4,q1,q2,q3)
            # print("zj1 ", zj1,"x1: ",xj1, "y1: ",yj1)
            # print("zj2 ", zj2,"x2: ",xj2, "y2: ",yj2)
            # print("zj3 ", zj3,"x3: ",xj3, "y3: ",yj3)
            
            # print("q2 ",q2)
            # print("q3 ",q3)
            # print("q1 ",q1)
            print("zj4 ", zj4,"x4: ",xj4, "y4: ",yj4)

        # background = cv2.imread("backround.jpg")
        # background=cv2.resize(background,(700,300))
        #  (not (compareArray(desired,prev_angle)))
        #send to arduino new angles
        if((time.time()-prevtime)>3 ):
              total=cmd_cb(desired,q1,q2,q3,q4)
              print(1)
              cmd=ArraytoString(total)
              cmd=cmd+'\r'
              print(cmd)
              arduinoData.write(cmd.encode())
              prevtime=time.time()
              time.sleep(2)
              if(abs(desired[3]-prev_angle[3])<1.5):
                  break

        # Show the frames
        cv2.imshow("frame right", frame_right) 
        cv2.imshow("frame left", frame_left)
        # cv2.imshow('Display',background)
        #cv2.imshow("mask right", mask_right_b) 
        #cv2.imshow("mask left", mask_left_b)
        print("q2 ",q2,"q3 ",q3,"q4 ",q4)

        # Hit "q" to close the window
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        #time.sleep(0.25)

# Release and destroy all windows before termination
cap_right.release()
cap_left.release()

cv2.destroyAllWindows()
