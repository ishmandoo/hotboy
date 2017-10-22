from Hotboy import Hotboy
from picamera import PiCamera
import time
import random

hotboy = Hotboy(camera=False)

with PiCamera() as camera:
	#camera = PiCamera()
	camera.resolution = (720, 480)
	#camera.start_preview()
	oldtogglestate = False
	while True:
		togglestate = hotboy.goSwitch()
		if oldtogglestate != togglestate:
			if togglestate == True:
				camera.start_recording('video' + str(random.randint(0,1000)) + '.h264') 
			else:
				camera.stop_recording()
		oldtogglestate = togglestate
		#camera.wait_recording(0.5)
		time.sleep(0.5)

	
