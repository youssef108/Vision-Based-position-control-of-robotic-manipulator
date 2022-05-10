import sys
import cv2
import numpy as np
import time


def add_HSV_filter(frame, color):

	# Blurring the frame
    blur = cv2.GaussianBlur(frame,(5,5),0) 

    # Converting RGB to HSV
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    if color =='b':
        l_b_blue = np.array([92,45 , 77])        # Lower limit for red ball
        u_b_blue = np.array([124, 184, 255])       # Upper limit for red ball
        mask = cv2.inRange(hsv, l_b_blue, u_b_blue)
    elif color == 'y':
        l_y= np.array([0,100,168])
        u_y =np.array([169,255,255])
        mask= cv2.inRange(hsv,l_y,u_y)
    elif color =='g':
        l_green= np.array([71,88,59])
        u_green =np.array([96,228,255])
        mask= cv2.inRange(hsv,l_green,u_green)
    elif color=='r':
        l_red= np.array([117,59,15])
        u_red =np.array([173,181,255])
        mask= cv2.inRange(hsv,l_red,u_red)


    #Erode followed by Dilate - Remove noise
    
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=4)
    mask=cv2.GaussianBlur(mask,(5,5),1)
    return mask

# img = cv2.VideoCapture(1,cv2.CAP_DSHOW)
# while True:
#     istrue, frame = img.read()
#     mask= add_HSV_filter(frame,'b')
#     cv2.imshow('img',mask)
#     mask2 = add_HSV_filter(frame,'r')
#     cv2.imshow('red',mask2)
#     if cv2.waitKey(1)==14:
#         break
