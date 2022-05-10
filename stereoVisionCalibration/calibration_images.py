## run this script to obtain images to use in camera calibration
import cv2

capright = cv2.VideoCapture(2,cv2.CAP_DSHOW)
cap2left = cv2.VideoCapture(1,cv2.CAP_DSHOW)
capright.set(3,800)
capright.set(4,720)
cap2left.set(3,800)
cap2left.set(4,720)
num = 0

while capright.isOpened():

    succes1, img = capright.read()
    succes2, img2 = cap2left.read()
    k = cv2.waitKey(5)

    if k == 27:
        break
    elif k == ord('s'): # wait for 's' key to save and exit
        cv2.imwrite('stereoVisionCalibration/Images/imagesLeft/imageL' + str(num) + '.png', img2)
        cv2.imwrite('stereoVisionCalibration/Images/imagesRight/imageR' + str(num) + '.png', img)
        print("images saved!")
        num += 1
 
    cv2.imshow('Img 1',img)
    cv2.imshow('Img 2',img2)

# Release and destroy all windows before termination
capright.release()
cap2left.release()

cv2.destroyAllWindows()
