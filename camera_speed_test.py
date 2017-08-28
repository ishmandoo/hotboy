from dronekit import connect
import time
import picamera

vehicle = connect("/dev/ttyACM0")

camera = picamera.PiCamera()

t1 = time.time()
camera.capture("test.jpg")
print vehicle.attitude
t2 time.time()

print t2-t1
