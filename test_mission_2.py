from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
import picamera

aTargetAltitude = 3

#vehicle = connect("/dev/ttyACM0")
vehicle = connect("tcp:127.0.0.1:5760")
camera = picamera.PiCamera()

time.sleep(15)

vehicle.mode = VehicleMode("GUIDED")

while not vehicle.mode == "GUIDED":
    print "waiting for guided mode"
    time.sleep(1)

while vehicle.channels["6"] < 1500:
    print "waiting for GO switch"
    time.sleep(1)
    break

vehicle.armed = True
time.sleep(5)
print vehicle.armed

homeLat = vehicle.location.global_frame.lat
homeLon = vehicle.location.global_frame.lon

if vehicle.armed == True:
    print "Taking off!"
    vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command
    #  after Vehicle.simple_takeoff will execute immediately).
    for i in range(10):
        print " Altitude: ", vehicle.location.global_relative_frame.alt
        if vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.95: #Trigger just below target alt.
            print "Reached target altitude"
            time.sleep(3)
            break
        time.sleep(1)

    for h in range(4,20,2):
        pos = LocationGlobalRelative(homeLat, homeLon, float(h))
        vehicle.simple_goto(pos)
        time.sleep(5)
        print " Altitude: ", vehicle.location.global_relative_frame.alt
        for i in range(10):
            camera.capture('img_' + str(h) + 'm_' + str(i) + '.jpg')
            time.sleep(1)

    vehicle.mode = VehicleMode("RTL")
    print vehicle.mode
