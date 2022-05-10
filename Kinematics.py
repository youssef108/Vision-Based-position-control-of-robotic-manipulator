from cmath import acos, atan, pi
from math import atan2,sqrt
#from cv2 import sqrt
import numpy as np
from scipy.optimize import fsolve
#l0=20
#l1=22
#l2=30
a1=18
a2=22
a3=13.5
a4=11
a5=16
q1_temp=0
SamplingDistance = 0.5
LearningRate=0.01
def relateCoordinates(x,y,z,xj1,yj1,zj1,xj2,yj2,zj2,xj3,yj3,zj3,xj4,yj4,zj4):
    #relate joint 2 and 3 to base 
    xj1=xj1-x
    yj1=yj1-y
    zj1=zj1-z
    xj2=xj2-x
    yj2= yj2-y
    zj2= zj2-z 
    xj3= xj3-x
    yj3= yj3-y
    zj3= zj3-z
    xj4= xj4-x
    yj4= yj4-y
    zj4= zj4-z
    return xj1,yj1,zj1,xj2,yj2,zj2,xj3,yj3,zj3,xj4,yj4,zj4
def forward_kinemtaics(var,*inputs):
    px,py,pz,q4=inputs
    q1,q2,q3=var
    eq1=22*round(np.cos(q2))*np.cos(q1) - 16*np.sin(q4)*(np.cos(q1)*np.cos(q2)*np.sin(q3) + np.cos(q1)*np.cos(q3)*np.sin(q2)) - 16*round(np.cos(q4))*(np.cos(q1)*np.sin(q2)*np.sin(q3) - np.cos(q1)*np.cos(q2)*np.cos(q3)) - (49*np.cos(q1)*np.sin(q2)*np.sin(q3))/2 + (49*round(np.cos(q3))*np.cos(q1)*np.cos(q2))/2-px
    eq2=22*round(np.cos(q2))*np.sin(q1) - 16*round(np.cos(q4))*(np.sin(q1)*np.sin(q2)*np.sin(q3) - np.cos(q2)*np.cos(q3)*np.sin(q1)) - 16*np.sin(q4)*(np.cos(q2)*np.sin(q1)*np.sin(q3) + np.cos(q3)*np.sin(q1)*np.sin(q2)) - (49*np.sin(q1)*np.sin(q2)*np.sin(q3))/2 + (49*round(np.cos(q3))*np.cos(q2)*np.sin(q1))/2 -py
    eq3=22*np.sin(q2) + (49*np.cos(q2)*np.sin(q3))/2 + 16*round(np.cos(q4))*(np.cos(q2)*np.sin(q3) + np.cos(q3)*np.sin(q2)) + (49*round(np.cos(q3))*np.sin(q2))/2 + 16*np.sin(q4)*(np.cos(q2)*np.cos(q3) - np.sin(q2)*np.sin(q3)) + 18 -pz
    # eq1=np.cos(q1)*(np.cos(q3)*(np.cos(q2)*((a3+a4)*np.cos(q4))-a5*np.sin(q2)*np.sin(q5))+np.sin(q2)*np.sin(q3)*((a3+a4)*np.sin(q4)+a5*np.cos(q4)*np.sin(q5))+a2*np.cos(q2)+a5*np.cos(q2)*np.sin(q3)*np.sin(q5))+np.sin(q1)*((a3+a4)*np.sin(q4)+a5*np.sin(q4)*np.cos(q5))-px
    # eq2=np.sin(q1)*(np.cos(q3)*(np.cos(q2)*((a3+a4)*np.cos(q4))-a5*np.sin(q2)*np.sin(q5))+np.sin(q2)*np.sin(q3)*((a3+a4)*np.sin(q4)+a5*np.cos(q4)*np.sin(q5))+a2*np.cos(q2)+a5*np.cos(q2)*np.sin(q3)*np.sin(q5))-np.cos(q1)*((a3+a4)*np.sin(q4)+a5*np.sin(q4)*np.cos(q5))-py
    # eq3=a1+a2*np.sin(q2)+np.cos(q3)*(np.sin(q2)*((a3+a4)*np.cos(q4)+a5*np.cos(q4)*np.cos(q5))-a5*np.cos(q2)*np.sin(q5))+np.sin(q3)*(np.cos(q2)*((a3+a4)*np.cos(q4)+a5*np.cos(q4)*np.cos(q5))+a5*np.sin(q2)*np.sin(q5)) -pz

    return [eq1,eq2,eq3]
def getAngles(xj1,yj1,zj1,xj2,yj2,zj2,xj3,yj3,zj3,xj4,yj4,zj4):
    q2=0
    q3=0
    q1=0
    q4=0
    # q1=np.arctan2(yj4,xj4)
    # q1=(q1*180)/pi
    # q1_j2=np.arctan2(yj2,xj2)
    # q1_j3=np.arctan2(yj3,xj3)
    # q1=q1_j2
    # if(q1_j2>q1_j3):
    #     q1=q1_j2
    #     q1=(q1*180)/pi

    #q1=np.arctan2(yj1,xj1)
    # q1=(q1*180)/pi
    q1=np.arctan2(yj2,xj2)
    q1=(q1*180)/pi
    if((xj2-xj1)==0):
        q2=90
    else:
        S=sqrt(xj2**2 + yj2**2)
        q2=np.arctan2((zj2-zj1),(S))
        q2=(q2*180)/pi

    if((xj3-xj2)==0):
        q3=90
    else:
        S=sqrt(xj3**2 +yj3**2)-sqrt(xj2**2 + yj2**2) 
        q3=np.arctan2((zj3-zj2),(S))
        q3=((q3*180)/pi - q2)

    if((xj4-xj3)==0):
        q4=90
    else:    
        S=sqrt(xj4**2 +yj4**2)-sqrt(xj3**2 + yj3**2) 
        q4=np.arctan2((zj4-zj3),(S))
        q4=(q4*180)/pi -(q2+q3)
    #using forward kinematics to get q1 and q5    
    q2_t=(q2*pi)/180 
    q3_t=(q3*pi)/180
    q4_t=(q4*pi)/180
    try: 
        q1,q2_t,q3_t=fsolve(forward_kinemtaics,(1,q2_t,q3_t),(xj4,yj4,zj4,q4_t))
        q1=(q1*180)/pi
        q1_temp=q1
    except:
        print("not able to calculate q1")
        q1=q1_temp
    return q1,q2,q3,q4

# q1=1.2
# q2=pi/2
# q3=-pi/2
# q4=pi/2
# q5=pi/2
# q1=116.87*(pi/180)
# q2=76.28*(pi/180)
# q3=40.59*(pi/180)
# q4=((0))*(pi/180)
# # input=(0,0,0,0,0,0,80.5)




# q1,q2,q3=fsolve(forward_kinemtaics,(1,pi/2,0),(16,0,64.5,pi/2))
# print(q1*180/pi)

# def Rumus_IK(X_End_Effector,Y_End_Effector,Z_End_Effector):
#     Theta_1=0
#     Theta_2=0
#     Theta_3=0
#     Theta_4=0
#     if (X_End_Effector > 0 and Z_End_Effector >= a1):
#         D = sqrt(X_End_Effector**2 + Y_End_Effector**2)
#         Theta_1 = (np.arctan2(Y_End_Effector,X_End_Effector))*(180.00/pi) #theta 1
#         d = D - a5
#         Zoffset = Z_End_Effector - a1
#         R = sqrt(d**2 + Zoffset**2)
#         alpha1 = (np.arccos(d/R))*(180.00/pi)
#         alpha2 = (np.arccos((a2**2 + R**2 - (a3+a4)**2)/(2*a2*R)))*(180.00/pi)
#         #Theta_2=(pow(a2,2) + pow(R,2) - pow((a3+a4),2))/(2*a2*R)
#         Theta_2 = (alpha1 + alpha2) #theta 2
#         Theta_3 = ((np.arccos(((a2**2) + ((a3+a4)**2) - (R**2))/(2*a2*(a3+a4))))*(180.00/pi)) #theta 3
#         #Theta_4 = (180.00 - ((180.00 - (alpha2 + Theta_3)) - alpha1)) #theta 4
#         Theta_4 = 360- (180 -(alpha2+Theta_3))-(180-(alpha1+90)) -90
#     elif (X_End_Effector > 0 and Z_End_Effector <= a1):
    
#         D = sqrt(pow(X_End_Effector,2) + pow(Y_End_Effector,2))
#         Theta_1 = (np.arctan2(Y_End_Effector,X_End_Effector))*(180.00/pi) #theta 1
#         d = D - a5
#         Zoffset = Z_End_Effector - a1
#         R = sqrt(pow(d,2) + pow(Zoffset,2))
#         alpha1 = (np.arccos(d/R))*(180.00/pi)
#         alpha2 = (np.arccos((pow(a2,2) + pow(R,2) - pow((a3+a4),2))/(2*a2*R)))*(180.00/pi)
#         Theta_2 = (alpha2 - alpha1) #theta 2
#         Theta_3 = ((np.arccos((pow(a2,2) + pow((a3+a4),2) - pow(R,2))/(2*a2*(a3+a4))))*(180.00/pi)) #theta 3
#         Theta_4 = 180.00 - ((180.00 - (alpha2 + Theta_3)) + alpha1) #theta 4
    
#     elif (X_End_Effector == 0 and Z_End_Effector >= a1):
    
#         D = sqrt(pow(X_End_Effector,2) + pow(Y_End_Effector,2))
#         Theta_1 = 90.00 #theta 1
#         d = D - a5
#         Zoffset = Z_End_Effector - a1
#         R = sqrt(pow(d,2) + pow(Zoffset,2))
#         alpha1 = (np.arccos(d/R))*(180.00/pi)
#         alpha2 = (np.arccos((pow(a2,2) + pow(R,2) - pow((a3+a4),2))/(2*a2*R)))*(180.00/pi)
#         Theta_2 = (alpha1 + alpha2) #theta 2
#         Theta_3 = ((np.arccos((pow(a2,2) + pow((a3+a4),2) - pow(R,2))/(2*a2*(a3+a4))))*(180.00/pi)) #theta 3
#         Theta_4 = 180.00 - ((180.00 - (alpha2 + Theta_3)) - alpha1) #theta 4
    
#     elif (X_End_Effector == 0 and Z_End_Effector <= a1):
    
#         D = sqrt(pow(X_End_Effector,2) + pow(Y_End_Effector,2))
#         Theta_1 = 90.00 #theta 1
#         d = D - a5
#         Zoffset = Z_End_Effector - a1
#         R = sqrt(pow(d,2) + pow(Zoffset,2))
#         alpha1 = (np.arccos(d/R))*(180.00/pi)
#         alpha2 = (np.arccos((pow(a2,2) + pow(R,2) - pow((a3+a4),2))/(2*a2*R)))*(180.00/pi)
#         Theta_2 = (alpha2 - alpha1) #theta 2
#         Theta_3 = ((np.arccos((pow(a2,2) + pow((a3+a4),2) - pow(R,2))/(2*a2*(a3+a4))))*(180.00/pi)) #theta 3
#         Theta_4 = 180.00 - ((180.00 - (alpha2 + Theta_3)) + alpha1) #theta 4
    
#     elif (X_End_Effector < 0 and Z_End_Effector >= a1):
    
#         D = sqrt(pow(X_End_Effector,2) + pow(Y_End_Effector,2))
#         Theta_1 = 90.00 + (90.00 - abs((np.arctan2(Y_End_Effector,X_End_Effector))*(180.00/pi))) #theta 1
#         d = D - a5
#         Zoffset = Z_End_Effector - a1
#         R = sqrt(pow(d,2) + pow(Zoffset,2))
#         alpha1 = (np.arccos(d/R))*(180.00/pi)
#         alpha2 = (np.arccos((pow(a2,2) + pow(R,2) - pow((a3+a4),2))/(2*a2*R)))*(180.00/pi)
#         Theta_2 = (alpha1 + alpha2) #theta 2
#         Theta_3 = ((np.arccos((pow(a2,2) + pow((a3+a4),2) - pow(R,2))/(2*a2*(a3+a4))))*(180.00/pi)) #theta 3
#         Theta_4 = 180.00 - ((180.00 - (alpha2 + Theta_3)) - alpha1) #theta 4
    
#     elif (X_End_Effector < 0 and Z_End_Effector <= a1):
    
#         D = sqrt(pow(X_End_Effector,2) + pow(Y_End_Effector,2))
#         Theta_1 = 90.00 + (90.00 - abs((np.arctan2(Y_End_Effector,X_End_Effector))*(180.00/pi))) #theta 1
#         d = D - a5
#         Zoffset = Z_End_Effector - a1
#         R = sqrt(pow(d,2) + pow(Zoffset,2))
#         alpha1 = (np.arccos(d/R))*(180.00/pi)
#         alpha2 = (np.arccos((pow(a2,2) + pow(R,2) - pow((a3+a4),2))/(2*a2*R)))*(180.00/pi)
#         Theta_2 = (alpha2 - alpha1) #theta 2
#         Theta_3 = ((np.arccos((pow(a2,2) + pow((a3+a4),2) - pow(R,2))/(2*a2*(a3+a4))))*(180.00/pi)) #theta 3
#         Theta_4 = 180.00 - ((180.00 - (alpha2 + Theta_3)) + alpha1) #theta 4
#     return Theta_1,Theta_2,Theta_3,Theta_4
# def PartialGradient(targetx,targety,targetz,angles,i):
#     angle = angles[i]
#     #Gradient : [F(x+SamplingDistance) - F(x)] / h
#     f_x = DistanceFromTarget(targetx,targety,targetz, angles)
#     angles[i] += SamplingDistance
#     f_x_plus_d = DistanceFromTarget(targetx,targety,targetz, angles)
#     gradient = (f_x_plus_d - f_x) / SamplingDistance
#     # Restores
#     angles[i] = angle
#     return gradient

# def InverseKinematics (targetx,targety,targetz,angles):
#     i=0
#     while (i<4):
#         # Gradient descent
#         # Update : Solution -= LearningRate * Gradient
#         gradient = PartialGradient(targetx,targety,targetz,angles,i)
#         angles[i] -= LearningRate * gradient
#         i+=1
#     return angles
# def DistanceFromTarget(targetx,targety,targetz,angles):
#     q1=angles[0]*(pi/180)
#     q2=angles[1]*(pi/180)
#     q3=angles[2]*(pi/180)
#     q4=angles[3]*(pi/180)

#     px=22*round(np.cos(q2))*np.cos(q1) - 16*np.sin(q4)*(np.cos(q1)*np.cos(q2)*np.sin(q3) + np.cos(q1)*np.cos(q3)*np.sin(q2)) - 16*round(np.cos(q4))*(np.cos(q1)*np.sin(q2)*np.sin(q3) - np.cos(q1)*np.cos(q2)*np.cos(q3)) - (49*np.cos(q1)*np.sin(q2)*np.sin(q3))/2 + (49*round(np.cos(q3))*np.cos(q1)*np.cos(q2))/2
#     py=22*round(np.cos(q2))*np.sin(q1) - 16*round(np.cos(q4))*(np.sin(q1)*np.sin(q2)*np.sin(q3) - np.cos(q2)*np.cos(q3)*np.sin(q1)) - 16*np.sin(q4)*(np.cos(q2)*np.sin(q1)*np.sin(q3) + np.cos(q3)*np.sin(q1)*np.sin(q2)) - (49*np.sin(q1)*np.sin(q2)*np.sin(q3))/2 + (49*round(np.cos(q3))*np.cos(q2)*np.sin(q1))/2
#     pz=22*np.sin(q2) + (49*np.cos(q2)*np.sin(q3))/2 + 16*round(np.cos(q4))*(np.cos(q2)*np.sin(q3) + np.cos(q3)*np.sin(q2)) + (49*round(np.cos(q3))*np.sin(q2))/2 + 16*np.sin(q4)*(np.cos(q2)*np.cos(q3) - np.sin(q2)*np.sin(q3)) + 18
#     d= sqrt((targetx-px)**2 + (targety-py)**2 +(targetz-pz)**2)
#     return d
# q1=8.589939101150065
# q2=63.99147202661492
# q3=-20.305653766106623
# q4=-8.751320698699205
# px=22*round(np.cos(q2))*np.cos(q1) - 16*np.sin(q4)*(np.cos(q1)*np.cos(q2)*np.sin(q3) + np.cos(q1)*np.cos(q3)*np.sin(q2)) - 16*round(np.cos(q4))*(np.cos(q1)*np.sin(q2)*np.sin(q3) - np.cos(q1)*np.cos(q2)*np.cos(q3)) - (49*np.cos(q1)*np.sin(q2)*np.sin(q3))/2 + (49*round(np.cos(q3))*np.cos(q1)*np.cos(q2))/2
# py=22*round(np.cos(q2))*np.sin(q1) - 16*round(np.cos(q4))*(np.sin(q1)*np.sin(q2)*np.sin(q3) - np.cos(q2)*np.cos(q3)*np.sin(q1)) - 16*np.sin(q4)*(np.cos(q2)*np.sin(q1)*np.sin(q3) + np.cos(q3)*np.sin(q1)*np.sin(q2)) - (49*np.sin(q1)*np.sin(q2)*np.sin(q3))/2 + (49*round(np.cos(q3))*np.cos(q2)*np.sin(q1))/2
# pz=22*np.sin(q2) + (49*np.cos(q2)*np.sin(q3))/2 + 16*round(np.cos(q4))*(np.cos(q2)*np.sin(q3) + np.cos(q3)*np.sin(q2)) + (49*round(np.cos(q3))*np.sin(q2))/2 + 16*np.sin(q4)*(np.cos(q2)*np.cos(q3) - np.sin(q2)*np.sin(q3)) + 18
# print(round(px))
# print(py)
# print(pz)
# print(" ")
# # Theta_1,Theta_2,Theta_3,Theta_4=Rumus_IK(21,28.9,29.3)
# # print(Theta_1)
# # print(Theta_2)
# # print(Theta_3)
# # print(Theta_4)
# targetx= 30
# targety= 20
# targetz= 50
# i=0
# angles=[0,90,0,0]
# while(i<5000):
#     angles=InverseKinematics(30,20,50,angles)
#     i+=1
# print(angles)
