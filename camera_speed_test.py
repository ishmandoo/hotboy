from dronekit import connect
import time
import picamera

vehicle = connect("/dev/ttyACM0")

camera = picamera.PiCamera()

print time.time()
camera.capture("test.jpg")
print vehicle.attitude
print time.time()
