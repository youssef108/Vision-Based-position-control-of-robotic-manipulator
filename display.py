import cv2 as cv
def display(frame,xj1,yj1,zj1,xj2,yj2,zj2,xj3,yj3,zj3,xj4,yj4,zj4,q1,q2,q3):
    #coordinates joint 1
    cv.putText(frame, "xj1:", (45,40), cv.FONT_ITALIC, 0.7, (255,255,255),2)
    cv.putText(frame, str(round(xj1,2)), (90,40), cv.FONT_ITALIC, 0.7, (255,255,255),2)
    cv.putText(frame, "yj1:", (260,40), cv.FONT_ITALIC, 0.7, (255,255,255),2)
    cv.putText(frame, str(round(yj1,2)), (305,40), cv.FONT_ITALIC, 0.7, (255,255,255),2)
    cv.putText(frame, "zj1:", (475,40), cv.FONT_ITALIC, 0.7, (255,255,255),2)
    cv.putText(frame, str(round(zj1,2)), (520,40), cv.FONT_ITALIC, 0.7, (255,255,255),2)
    #coordinates joint 2
    cv.putText(frame, "xj2:", (45,100), cv.FONT_ITALIC, 0.7, (255,255,255),2)
    cv.putText(frame, str(round(xj2,2)), (90,100), cv.FONT_ITALIC, 0.7, (255,255,255),2)
    cv.putText(frame, "yj2:", (260,100), cv.FONT_ITALIC, 0.7, (255,255,255),2)
    cv.putText(frame, str(round(yj2,2)), (305,100), cv.FONT_ITALIC, 0.7, (255,255,255),2)
    cv.putText(frame, "zj2:", (475,100), cv.FONT_ITALIC, 0.7, (255,255,255),2)
    cv.putText(frame, str(round(zj2,2)), (520,100), cv.FONT_ITALIC, 0.7, (255,255,255),2)
    #coordinates joint 3
    cv.putText(frame, "xj3:", (45,160), cv.FONT_ITALIC, 0.7, (255,255,255),2)
    cv.putText(frame, str(round(xj3,2)), (90,160), cv.FONT_ITALIC, 0.7, (255,255,255),2)
    cv.putText(frame, "yj3:", (260,160), cv.FONT_ITALIC, 0.7, (255,255,255),2)
    cv.putText(frame, str(round(yj3,2)), (305,160), cv.FONT_ITALIC, 0.7, (255,255,255),2)
    cv.putText(frame, "zj3:", (475,160), cv.FONT_ITALIC, 0.7, (255,255,255),2)
    cv.putText(frame, str(round(zj3,2)), (520,160), cv.FONT_ITALIC, 0.7, (255,255,255),2)
    #coordinates joint 4
    cv.putText(frame, "xj4:", (45,220), cv.FONT_ITALIC, 0.7, (255,255,255),2)
    cv.putText(frame, str(round(xj4,2)), (90,220), cv.FONT_ITALIC, 0.7, (255,255,255),2)
    cv.putText(frame, "yj4:", (260,220), cv.FONT_ITALIC, 0.7, (255,255,255),2)
    cv.putText(frame, str(round(yj4,2)), (305,220), cv.FONT_ITALIC, 0.7, (255,255,255),2)
    cv.putText(frame, "zj4:", (475,220), cv.FONT_ITALIC, 0.7, (255,255,255),2)
    cv.putText(frame, str(round(zj4,2)), (520,220), cv.FONT_ITALIC, 0.7, (255,255,255),2)
    #angles
    #cv.putText(frame, "Angles:", (45,190), cv.FONT_ITALIC, 0.7, (255,255,255),2)
    cv.putText(frame, "q1:", (45,280), cv.FONT_ITALIC, 0.7, (255,255,255),2)
    cv.putText(frame, str(round(q1,2)), (90,280), cv.FONT_ITALIC, 0.7, (255,255,255),2)
    cv.putText(frame, "q2:", (260,280), cv.FONT_ITALIC, 0.7, (255,255,255),2)
    cv.putText(frame, str(round(q2,2)), (305,280), cv.FONT_ITALIC, 0.7, (255,255,255),2)
    cv.putText(frame, "q3:", (475,280), cv.FONT_ITALIC, 0.7, (255,255,255),2)
    cv.putText(frame, str(round(q3,2)), (520,280), cv.FONT_ITALIC, 0.7, (255,255,255),2)
    

    
    









# img = cv.imread("backround.jpg")
# img=cv.resize(img,(700,400))
# display(img,1,2,3,4,5,6,7,8,9,0,4,5,6,7,8)
# cv.imshow('im',img)
# cv.waitKey(0)