"""
Use with PID class from:
https://github.com/ivmech/ivPID
"""

import PID
import picamera
import dronekit
from pymavlink import mavutil


#===============================================================================
def send_body_ned_velocity(velocity_x, velocity_y, velocity_z, duration=0):
	"""
    Move vehicle in direction based on specified velocity vectors.
	REFS: https://stackoverflow.com/questions/39695181/how-to-do-go-to-left-right-forward-backward-with-python-dronekit;
	http://python.dronekit.io/guide/copter/guided_mode.html#guided-mode-copter-velocity-control
    """
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,       # time_boot_ms (not used)
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_FRAME_BODY_OFFSET_NED, # frame needs to be MAV_FRAME_BODY_NED for forward/back left/right control. -- Might just be MAV_FRAME_BODY_NED? 
        0b0000111111000111, # type_mask (only speeds enabled) -- for pos use 111000 for right six
        0, 0, 0, # x, y, z positions (not used)
        velocity_x, velocity_y, velocity_z, # m/s
        0, 0, 0, # x, y, z acceleration (not supported yet, ignored in GCS_Mavlink)
        0, 0)    # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink)
	# send command to vehicle on 1 Hz cycle
    for x in range(0,duration):
        vehicle.send_mavlink(msg)
        time.sleep(1)
#===============================================================================



vehicle = dronekit.connect("/dev/ttyACM0")
# MORE VEHICLE STUFF HERE

#PIDs for x and y image axes with inputs Kp, Ki, Kd
xpid = PID.PID(0.2, 0.0, 0.0) # Play with these gain parameters
ypid = PID.PID(0.2, 0.0, 0.0)

while True:

	# Insert image capture code here and return xavg and yavg (as in pitrackobject), which are the process variables

	# I *think* PID class defaults to zero setpoint
	xerr = (Floor of the camera resolution width/2) - xavg
	yerr = (Floor of the camera resolution height/2) - yavg

	xpid.update(xerr)
	ypid.update(yerr)

	# Override any ongoing movement commands here (if not automatically overridden by the following)


	"""
	Here, command the drone to move. How much is TBD by xpid.output, ypid.output,
	and altitude.

	Easiest approach might be designating movement y meters forward and x meters to the right
	in the reference frame MAV_FRAME_BODY_OFFSET_NED (could also tweak x and y velocities):

	OR:
	Set target lat and lon based on ypid.output, xpid.output, and altitude
	"""
