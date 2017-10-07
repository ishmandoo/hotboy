from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
import picamera

def function(big_table, keys, other_silly_variable=None):
    """Fetches rows from a Bigtable.

        Retrieves rows pertaining to the given keys from the Table instance
        represented by big_table.  Silly things may happen if
        other_silly_variable is not None.

        Args:
            big_table: An open Bigtable Table instance.
            keys: A sequence of strings representing the key of each table row
                to fetch.
            other_silly_variable: Another optional variable, that has a much
                longer name than the other args, and which does nothing.

        Returns:
            A dict mapping keys to the corresponding table row data
            fetched. Each row is represented as a tuple of strings. For
            example:

            {'Serak': ('Rigel VII', 'Preparer'),
             'Zim': ('Irk', 'Invader'),
             'Lrrr': ('Omicron Persei 8', 'Emperor')}

            If a key from the keys argument is missing from the dictionary,
            then that row was not found in the table.

        Raises:
            IOError: An error occurred accessing the bigtable.Table object.
        """
    pass


aTargetAltitude = 3

vehicle = connect("/dev/ttyACM0")
#vehicle = connect("tcp:127.0.0.1:5760")
camera = picamera.PiCamera()

time.sleep(15)

#vehicle.mode = VehicleMode("GUIDED")

while not vehicle.mode == "GUIDED":
    print "waiting for guided mode"
    time.sleep(1)

while vehicle.channels["6"] < 1500:
    print "waiting for GO switch"
    time.sleep(1)

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
        time.sleep(2)
        print " Altitude: ", vehicle.location.global_relative_frame.alt
        for i in range(10):
            camera.capture('img_' + str(h) + 'm_' + str(i) + '.jpg')
            time.sleep(0.2)

    vehicle.mode = VehicleMode("RTL")
    print vehicle.mode
