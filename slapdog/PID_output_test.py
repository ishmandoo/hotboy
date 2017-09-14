# Based on pitrackobject
# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
import PID

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (720, 480)
#camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(720, 480))
#rawCapture = PiRGBArray(camera)
picnum = 0
def draw_circle(frame,x,y):
	cv2.circle(frame,(x,y),20,(255,0,0),2)
# allow the camera to warmup
time.sleep(0.1)

#PIDs for x and y image axes with inputs Kp, Ki, Kd
xpid = PID.PID(0.5, 0.0, 0.0) # Play with these gain parameters
ypid = PID.PID(0.5, 0.0, 0.0)

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
		#print "x:" + str(xavg) + " y: " + str(yavg)
		draw_circle(frame, int(xavg), int(yavg))

		# I *think* PID class defaults to zero setpoint
		# Might need to swap 0 and 1 indices below; yerr might be opposite sign...
		xerr = xavg - np.floor(camera.resolution[0]/2)
		yerr = np.floor(camera.resolution[1]/2) - yavg

		xpid.update(xerr)
		ypid.update(yerr)

		# print xpid.output and ypid.output
		print "x_err: " + str(xerr) + " | x_out: " + str(xpid.output) + " | y_err: " + str(yerr) + " | y_out: " + str(ypid.output)

		time.sleep(2)

	"""
	cv2.imwrite("current_img.jpg",frame)
	cv2.imwrite("pics/img" + str(picnum) + ".jpg",frame)
	picnum += 1
	# Bitwise-AND mask and original image
	res = cv2.bitwise_and(frame,frame, mask= mask)

		# show the frame
		#cv2.imshow("Frame", image)
	key = cv2.waitKey(1000) & 0xFF

		# clear the stream in preparation for the next frame
	rawCapture.truncate(0)

		# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break
	"""
