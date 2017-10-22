from Hotboy import Hotboy
from picamera import PiCamera
import time
import random

hotboy = HotBoy(camera=False)
camera = PiCamera()

oldtogglestate = False
while True:
	togglestate = hotboy.goSwitch()
	if oldtogglestate != togglestate:
		if togglestate == True:
			camera.start_recording('video' + str(random.randint(0,1000)) + '.h264') 
		else:
			camera.stop_recording()

	time.sleep(0.5)

	
