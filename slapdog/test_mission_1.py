from dronekit import connect, VehicleMode
import time

aTargetAltitude = 3

#vehicle = connect("/dev/ttyACM0")
vehicle = connect("tcp:127.0.0.1:5760")

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

    vehicle.mode = VehicleMode("RTL")
    print vehicle.mode
