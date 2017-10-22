from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
import picamera
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
from threading import Thread


class Hotboy():

    def __init__(self,port="/dev/ttyACM0", camera=True, activate=False):
        self.vehicle = connect(port, wait_ready=True)
        self.homeLat = vehicle.location.global_frame.lat
        self.homeLon = vehicle.location.global_frame.lon
        self.activated = False
        if activate:
            self.activate()
        if camera:
            self.initCamera()

    def __del__(self):
        self.vehicle.close()
        self.stream.close()
        self.rawCapture.close()
        self.camera.close()
        self.stopped = True

    def initCamera(self):
        # based on https://github.com/jrosebr1/imutils/blob/master/imutils/video/pivideostream.py
        self.camera = PiCamera()
        self.camera.resolution = (720, 480)
        #self.camera.framerate = framerate
        self.rawCapture = PiRGBArray(camera, size=(720, 480))
        self.stream = self.camera.capture_continuous(self.rawCapture,
            format="bgr", use_video_port=True)
        # start the thread to read frames from the video stream
        self.frame = np.zeros((480,720,3), dtype=np.uint8)
        self.stopped = False
        t = Thread(target=self.cameraLoop, args=())
        t.daemon = True
        t.start()


    def cameraLoop(self):
        # keep looping infinitely until the thread is stopped
        for f in self.stream:
            # grab the frame from the stream and clear the stream in
            # preparation for the next frame
            self.frame = f.array
            self.rawCapture.truncate(0)

            # if the thread indicator variable is set, stop the thread
            # and resource camera resources
            if self.stopped:
                self.stream.close()
                self.rawCapture.close()
                self.camera.close()
                return


    def getFrame(self):
        return self.frame

    def activate(self, aTargetAltitude):
        """
        Arms vehicle
        Sets self.activate to True
        """
        print "Basic pre-arm checks"
        # Don't try to arm until autopilot is ready
        while not self.vehicle.is_armable:
            print " Waiting for vehicle to initialise..."
            time.sleep(1)

        print "Arming motors"
        # Copter should arm in GUIDED mode
        self.vehicle.mode    = VehicleMode("GUIDED")

        while not vehicle.mode == "GUIDED":
            print "waiting for guided mode"
            time.sleep(1)
        self.vehicle.armed   = True

        # Confirm vehicle armed before attempting to take off
        while not vehicle.armed:
            print " Waiting for arming..."
            time.sleep(1)
        self.activated = True

    def takeoff(self, altitude):
        self.vehicle.simple_takeoff(altitude)

    def RTL(self, altitude=None):
        if altitude:
            self.vehicle.parameters['RTL_ALT'] = 0
        self.vehicle.mode = VehicleMode("RTL")

    def goSwitch(self):
        return vehicle.channels["6"] > 1500

    def sendVelocity(self, vx, vy, vz):
        '''Ref: http://python.dronekit.io/guide/copter/guided_mode.html
         North, East, Down coordinate system
         May need updating every three seconds to persist? 
        '''
        msg = self.vehicle.message_factory.set_position_target_local_ned_encode(
            0,       # time_boot_ms (not used)
            0, 0,    # target system, target component
            mavutil.mavlink.MAV_FRAME_LOCAL_NED, # frame
            0b0000111111000111, # type_mask (only speeds enabled)
            0, 0, 0, # x, y, z positions (not used)
            vx, vy, vz, # x, y, z velocity in m/s
            0, 0, 0, # x, y, z acceleration (not supported yet, ignored in GCS_Mavlink)
            0, 0)    # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink)





