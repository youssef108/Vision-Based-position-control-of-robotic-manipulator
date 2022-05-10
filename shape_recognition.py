
import cv2
import numpy as np
import imutils
import HSV_filter as filter

def find_circles(frame, mask):
    mask=cv2.GaussianBlur(mask,(11,11), 1)
    contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    center = None

    # Only proceed if at least one contour was found
    if len(contours) > 0:
        # Find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)       #Finds center point
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # Only proceed if the radius is greater than a minimum value
        if radius > 10:
            # Draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius),
            	(0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 0), -1)


    return center
# img= cv2.VideoCapture(1,cv2.CAP_DSHOW)
# while True:
#     istrue, frame = img.read()
#     mask= filter.add_HSV_filter(frame,'b')
#     cv2.imshow('img',mask)
#     mask2 = filter.add_HSV_filter(frame,'r')
#     #cv2.imshow('red',mask2)
#     find_circles(frame , mask)
#     find_circles(frame,mask2)
#     cv2.imshow('frame',frame)
#     if cv2.waitKey(1)==14:
#         break