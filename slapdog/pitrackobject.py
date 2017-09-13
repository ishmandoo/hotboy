# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (720, 480)
#camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(720, 480))
#rawCapture = PiRGBArray(camera)

# allow the camera to warmup
time.sleep(0.1)

# capture frames from the camera
for piframe in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	frame = piframe.array

	# Convert BGR to HSV
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	# define range of color in HSV
	#lower_blue = np.array([50,50,50])
	#upper_blue = np.array([70,255,255])


	x = np.arange(frame.shape[1])
	y = np.arange(frame.shape[0])
	xv, yv = np.meshgrid(x, y, sparse=False)


	#currently set for orange frisbee
	lower_color = np.array([25,0,180])
	upper_color = np.array([65,255,255])
	# Threshold the HSV image to get only desired colors
	mask = cv2.inRange(hsv, lower_color, upper_color)

	N = np.sum(mask)
	if N >= 5 :
		xavg = np.sum( mask * xv) / N
		yavg = np.sum( mask * yv) / N
		print "x:" + str(xavg) + " y: " + str(yavg)
		draw_circle(frame, int(xavg), int(yavg))


	cv2.imwrite("current_img.jpg",frame)
	# Bitwise-AND mask and original image
	res = cv2.bitwise_and(frame,frame, mask= mask)

		# show the frame
		#cv2.imshow("Frame", image)
	key = cv2.waitKey(1) & 0xFF

		# clear the stream in preparation for the next frame
	rawCapture.truncate(0)

		# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break
