import sys
import cv2
import numpy as np
import time

def find_depth(circle_right, circle_left, frame_right, frame_left, baseline,f, alpha):
    zDepth=0
    # CONVERT FOCAL LENGTH f FROM [mm] TO [pixel]:
    height_right, width_right, depth_right = frame_right.shape
    height_left, width_left, depth_left = frame_left.shape
    f_pixel=879.4197998
    # if width_right == width_left:
    #     f_pixel = (width_right * 0.5) / np.tan(alpha * 0.5 * np.pi/180)

    # else:
    #     print('Left and right camera frames do not have the same pixel width')
    if(circle_left!=None and circle_right !=None):
        x_right = circle_right[0]
        x_left = circle_left[0]
        disparity=0
    # CALCULATE THE DISPARITY:
        disparity = x_left-x_right      #Displacement between left and right frames [pixels]
    #if(disparity!=None):
    # CALCULATE DEPTH z:
        if(disparity!=None):
            zDepth = (f_pixel*baseline)/disparity #Depth in [cm]
            xcoordinate= (x_left*zDepth)/f_pixel
            y_left=(circle_left[1]-720)*-1
            ycoordinate=(y_left*zDepth)/f_pixel
            #relate to robot axis
            if(zDepth!=None):
                temp= zDepth
                zDepth = ycoordinate
                ycoordinate= temp
                #relate traslation
                return abs(zDepth), xcoordinate, ycoordinate
            else:
                return 0,0,0


