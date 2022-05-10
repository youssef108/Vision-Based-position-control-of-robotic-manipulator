import cv2 as cv
import numpy as np
def empty(a):
    pass
img = cv.VideoCapture(1,cv.CAP_DSHOW)
path = "photos\cars.jpg"
cv.namedWindow('TrackBars')
cv.resizeWindow('TrackBars',640,240)
cv.createTrackbar("hue Min","TrackBars",49,179,empty)
cv.createTrackbar("hue max","TrackBars",93,179,empty)
cv.createTrackbar("sat Min","TrackBars",52,255,empty)
cv.createTrackbar("sat max","TrackBars",250,255,empty)
cv.createTrackbar("val Min","TrackBars",58,255,empty)
cv.createTrackbar("val Max","TrackBars",255,255,empty)
while True:
    isTrue ,frame = img.read()
    imghsv= cv.cvtColor(frame,cv.COLOR_BGR2HSV)
    h_min=cv.getTrackbarPos("hue Min","TrackBars")
    h_max=cv.getTrackbarPos("hue max","TrackBars")
    s_min=cv.getTrackbarPos("sat Min","TrackBars")
    s_max=cv.getTrackbarPos("sat max","TrackBars") 
    v_min=cv.getTrackbarPos("val Min","TrackBars")
    v_max=cv.getTrackbarPos("val Max","TrackBars")
    #print(h_min,h_max)
    lower= np.array([h_min,s_min,v_min])
    upper=np.array([h_max,s_max,v_max])
    mask=cv.inRange(imghsv,lower,upper)
    imgresult=cv.bitwise_and(frame,frame,mask=mask)
    cv.imshow('hsv',imghsv)
    cv.imshow('mask',mask)
    cv.imshow('img',frame)
    cv.imshow('img',imgresult)
    cv.waitKey(1)