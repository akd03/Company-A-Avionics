from pymavlink import mavutil
import time
from simple_pid import PID
import numpy as np

master = mavutil.mavlink_connection('tcp:127.0.0.1:5763')  

m = master.mav.command_long_encode(
        master.target_system, master.target_component,
        511, 0,
        30, # The MAVLink message ID
        20000, # The interval between two messages in microseconds. Set to -1 to disable and 0 to request default rate.
        0, 
        0, 
        0, 
        0, # Unused parameters
        0, # Target address of message stream - 0 default
    )

master.mav.send(m)
print("CONNECTED!")

# Create a PID controller instance for pitch stabilization
pid = PID(50, 0.8, 2, setpoint=0)  # Adjust Kp, Ki, Kd values accordingly
#pid.output_limits = (-500, 500)  # Define output limits for the servo

master.mav.param_set_send(
    master.target_system, master.target_component,
    b'SERVO2_FUNCTION',
    0,
    mavutil.mavlink.MAV_PARAM_TYPE_REAL32
)

master.mav.param_set_send(
    master.target_system, master.target_component,
    b'SERVO1_FUNCTION',
    0,
    mavutil.mavlink.MAV_PARAM_TYPE_REAL32
)

master.mav.param_set_send(
    master.target_system, master.target_component,
    b'SERVO4_FUNCTION',
    0,
    mavutil.mavlink.MAV_PARAM_TYPE_REAL32
)


def adjust_elevator(servo_number, pwm_value):

    master.mav.command_long_send(

        master.target_system, master.target_component,

        mavutil.mavlink.MAV_CMD_DO_SET_SERVO,

        0,

        servo_number,

        pwm_value,

        0, 0, 0, 0, 0

    )

master.mav.param_set_send(
    master.target_system, master.target_component,
    b'SERVO3_FUNCTION',
    0,
    mavutil.mavlink.MAV_PARAM_TYPE_REAL32
)

adjust_elevator(2,1800)

#time.sleep(2)

adjust_elevator(3,1250) #throttle setting (1100 for low pitch, 1250 mid pitch, 1400 for high pitch)

def get_attitude():

    master.mav.request_data_stream_send(master.target_system, master.target_component,

                                        mavutil.mavlink.MAV_DATA_STREAM_EXTENDED_STATUS, 1, 1)

    msg = master.recv_match(type='ATTITUDE', blocking=True)

    if msg:

        return msg.pitch, msg.yaw, msg.roll

    else:

        return None, None, None


master.mav.request_data_stream_send(master.target_system, master.target_component,

                                        mavutil.mavlink.MAV_DATA_STREAM_RC_CHANNELS, 1, 1)

pid_radians=0*(np.pi/180)
pid.setpoint=pid_radians

while True:
    time.sleep(0.05)
    msg2 = master.recv_match(type='SERVO_OUTPUT_RAW', blocking=True).to_dict()
    print(f"Servo 2: {msg2['servo2_raw']}")
    get_attitude()
    current_pitch, current_yaw, current_roll = get_attitude()
    print(f"Current Pitch: {current_pitch}")  #, Current Yaw: {current_yaw}, Current Roll: {current_roll}")
    #pitch_error=(pid.setpoint-current_pitch)
    #print (pitch_error)
    control = pid(current_pitch) 
    print("PID_OUTPUT:", control)
    new_servo = 1500 + ((control))    
    print("Servo_PWM:", new_servo)
    adjust_elevator(2, new_servo)
    time.sleep(0.05)

