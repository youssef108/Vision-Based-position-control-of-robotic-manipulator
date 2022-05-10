from cv2 import CAP_DSHOW
import numpy as np 
import cv2


# Check for left and right camera IDs
# These values can change depending on the system
CamL_id = 1 # Camera ID for left camera
CamR_id = 2 # Camera ID for right camera

CamL= cv2.VideoCapture(CamL_id,CAP_DSHOW)
CamR= cv2.VideoCapture(CamR_id,CAP_DSHOW)
CamL.set(3,800)
CamL.set(4,720)
CamR.set(3,800)
CamR.set(4,720)
# Reading the mapping values for stereo image rectification
cv_file = cv2.FileStorage()
cv_file.open('stereoMap.xml', cv2.FileStorage_READ)

stereoMapL_x = cv_file.getNode('stereoMapL_x').mat()
stereoMapL_y = cv_file.getNode('stereoMapL_y').mat()
stereoMapR_x = cv_file.getNode('stereoMapR_x').mat()
stereoMapR_y = cv_file.getNode('stereoMapR_y').mat()
cv_file.release()

def nothing(x):
    pass

cv2.namedWindow('disp1',cv2.WINDOW_NORMAL)
cv2.resizeWindow('disp1',600,600)

cv2.createTrackbar('numDisparities','disp1',1,17,nothing)
cv2.createTrackbar('blockSize','disp1',5,50,nothing)
cv2.createTrackbar('preFilterType','disp1',1,1,nothing)
cv2.createTrackbar('preFilterSize','disp1',2,25,nothing)
cv2.createTrackbar('preFilterCap','disp1',5,62,nothing)
cv2.createTrackbar('textureThreshold','disp1',10,100,nothing)
cv2.createTrackbar('uniquenessRatio','disp1',15,100,nothing)
cv2.createTrackbar('speckleRange','disp1',0,100,nothing)
cv2.createTrackbar('speckleWindowSize','disp1',3,25,nothing)
cv2.createTrackbar('disp12MaxDiff','disp1',5,25,nothing)
cv2.createTrackbar('minDisparity','disp1',5,25,nothing)

# Creating an object of StereoBM algorithm
stereo = cv2.StereoBM_create()

while True:

	# Capturing and storing left and right camera images
	retL, imgL= CamL.read()
	retR, imgR= CamR.read()
	
	# Proceed only if the frames have been captured
	if retL and retR:
		imgR_gray = cv2.cvtColor(imgR,cv2.COLOR_BGR2GRAY)
		imgL_gray = cv2.cvtColor(imgL,cv2.COLOR_BGR2GRAY)

		# Applying stereo image rectification on the left image
		Left_nice= cv2.remap(imgL_gray,
							stereoMapL_x,
							stereoMapL_y,
							cv2.INTER_LANCZOS4,
							cv2.BORDER_CONSTANT,
							0)
		
		# Applying stereo image rectification on the right image
		Right_nice= cv2.remap(imgR_gray,
							stereoMapR_x,
							stereoMapR_y,
							cv2.INTER_LANCZOS4,
							cv2.BORDER_CONSTANT,
							0)

		# Updating the parameters based on the trackbar positions
		numDisparities = cv2.getTrackbarPos('numDisparities','disp1')*16
		blockSize = cv2.getTrackbarPos('blockSize','disp1')*2 + 5
		preFilterType = cv2.getTrackbarPos('preFilterType','disp1')
		preFilterSize = cv2.getTrackbarPos('preFilterSize','disp1')*2 + 5
		preFilterCap = cv2.getTrackbarPos('preFilterCap','disp1')
		textureThreshold = cv2.getTrackbarPos('textureThreshold','disp1')
		uniquenessRatio = cv2.getTrackbarPos('uniquenessRatio','disp1')
		speckleRange = cv2.getTrackbarPos('speckleRange','disp1')
		speckleWindowSize = cv2.getTrackbarPos('speckleWindowSize','disp1')*2
		disp12MaxDiff = cv2.getTrackbarPos('disp12MaxDiff','disp1')
		minDisparity = cv2.getTrackbarPos('minDisparity','disp1')
		
		# Setting the updated parameters before computing disparity map
		stereo.setNumDisparities(numDisparities)
		stereo.setBlockSize(blockSize)
		stereo.setPreFilterType(preFilterType)
		stereo.setPreFilterSize(preFilterSize)
		stereo.setPreFilterCap(preFilterCap)
		stereo.setTextureThreshold(textureThreshold)
		stereo.setUniquenessRatio(uniquenessRatio)
		stereo.setSpeckleRange(speckleRange)
		stereo.setSpeckleWindowSize(speckleWindowSize)
		stereo.setDisp12MaxDiff(disp12MaxDiff)
		stereo.setMinDisparity(minDisparity)

		# Calculating disparity using the StereoBM algorithm
		disparity = stereo.compute(Left_nice,Right_nice)
		# NOTE: compute returns a 16bit signed single channel image,
		# CV_16S containing a disparity map scaled by 16. Hence it 
		# is essential to convert it to CV_32F and scale it down 16 times.

		# Converting to float32 
		disparity = disparity.astype(np.float32)

		# Scaling down the disparity values and normalizing them 
		disparity = (disparity/16.0 - minDisparity)/numDisparities

		# Displaying the disparity map
		cv2.imshow("disp",disparity)

		# Close window using esc key
		if cv2.waitKey(1) == 27:
			break
	
	# else:
	# 	CamL= cv2.VideoCapture(CamL_id)
	# 	CamR= cv2.VideoCapture(CamR_id)

print("Saving depth estimation paraeters ......")

cv_file = cv2.FileStorage("depth_estmation_params_py.xml", cv2.FILE_STORAGE_WRITE)
cv_file.write("numDisparities",numDisparities)
cv_file.write("blockSize",blockSize)
cv_file.write("preFilterType",preFilterType)
cv_file.write("preFilterSize",preFilterSize)
cv_file.write("preFilterCap",preFilterCap)
cv_file.write("textureThreshold",textureThreshold)
cv_file.write("uniquenessRatio",uniquenessRatio)
cv_file.write("speckleRange",speckleRange)
cv_file.write("speckleWindowSize",speckleWindowSize)
cv_file.write("disp12MaxDiff",disp12MaxDiff)
cv_file.write("minDisparity",minDisparity)
cv_file.write("M",39.075)
cv_file.release()