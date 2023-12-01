from pymavlink import mavutil
import time
from simple_pid import PID

# Establish MAVLink connection
master = mavutil.mavlink_connection('tcp:127.0.0.1:5763')

# Function to adjust elevator servo
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
    b'SERVO2_FUNCTION',
    0,
    mavutil.mavlink.MAV_PARAM_TYPE_REAL32
)


# Function to retrieve attitude data
def get_attitude():
    master.mav.request_data_stream_send(master.target_system, master.target_component,
                                        mavutil.mavlink.MAV_DATA_STREAM_EXTENDED_STATUS, 1, 1)
    msg = master.recv_match(type='ATTITUDE', blocking=True)
    if msg:
        return msg.pitch, msg.yaw, msg.roll
    else:
        return None, None, None

# Create a PID controller instance for pitch stabilization
pid = PID(0.1, 0.1, 0.005, setpoint=0)  # Adjust Kp, Ki, Kd values accordingly 
#pid.output_limits = (-500, 500)  # Define output limits for the servo

#WHAT IS THE SETPOINT VALUE IN? IS IT AN ANGLE OR A PWM VALUE? It is an angle


# Range to make the aircraft pitch up
for us in range(1500, 1634, int(100/15)):

    adjust_elevator(2, us)  #DONE TO CHANGE THE PITCH, in PWM because that was the only way for mission planner?
    time.sleep(0.0125)
    msg2 = master.recv_match(type='SERVO_OUTPUT_RAW', blocking=True).to_dict()
    print(f"Servo 2: {msg2['servo2_raw']}")
    get_attitude()
    current_pitch, _, _ = get_attitude()
    C_Pitch = current_pitch * (180/3.142)
    #pid_output = pid(0 - current_pitch)  # Calculate PID output based on pitch error
    print(f"Current Pitch: {C_Pitch}")



master.mav.param_set_send(
    master.target_system, master.target_component,
    b'SERVO2_FUNCTION',
    19,
    mavutil.mavlink.MAV_PARAM_TYPE_REAL32

)
    
''' 
   pitch_error = 0 - C_Pitch  
    print("Pitch error:", pitch_error)
    pid_output = pid(pitch_error)  #assuming simple_pid algorithm knows how to do it for aircrafts and is giving us an elevator 
    
    pid_output_PWM = pid_output * (100/15)  #remember that this is an elevator deflection
    print("test PID output:", pid_output_PWM)
    adjust_elevator(2, pid_output_PWM)  # Adjust elevator using PID output
    time.sleep(0.1)
    

#WHAT IS THE PID_OUTPUT VALUE IN? DOES IT COME OUT IN PWM LIKE US? IF NOT WHAT DOES IT COME OUT IN AND THEREFORE AFTER THAT HOW CAN WE CONVERT IT?


adjust_elevator(2, 500/15)  #DONE TO CHANGE THE PITCH, in PWM because that was the only way for mission planner?
time.sleep(0.0125)
msg2 = master.recv_match(type='SERVO_OUTPUT_RAW', blocking=True).to_dict()
print(f"Servo 2: {msg2['servo2_raw']}")
get_attitude()
current_pitch, _, _ = get_attitude()
C_Pitch = current_pitch * (180/3.142)
#pid_output = pid(0 - current_pitch)  # Calculate PID output based on pitch error
pitch_error = 0 - C_Pitch  #ADD CONVERSION TO DEGREES
print("Pitch error:", pitch_error)
pid_output = pid(pitch_error)  #assuming simple_pid algorithm knows how to do it for aircrafts and is giving us an elevator 
    
pid_output_PWM = pid_output * (100/15)  #remember that this is an elevator deflection
print("test PID output:", pid_output_PWM)
adjust_elevator(2, pid_output_PWM)  # Adjust elevator using PID output
time.sleep(0.1)
print(f"Current Pitch: {C_Pitch}")




# Range to make the aircraft pitch down
for us in range(1550, 1500, -10):
    adjust_elevator(2, us)
    time.sleep(0.125)
    msg2 = master.recv_match(type='SERVO_OUTPUT_RAW', blocking=True).to_dict()
    print(f"Servo 2: {msg2['servo2_raw']}")
    get_attitude()
    current_pitch, _, _ = get_attitude()
    #pid_output = pid(0 - current_pitch)  # Calculate PID output based on pitch error
    pitch_error = 0 - current_pitch
    print("Pitch error", pitch_error)
    pid_output = pid(pitch_error)
    print
    adjust_elevator(2, int(pid_output))  # Adjust elevator using PID output
    time.sleep(0.1)
    print(f"Current Pitch: {current_pitch}")






# Continuous reception of MAVLink messages and stabilization using PID
while True:
    msg = master.recv_match()
    if not msg:
        continue
    if msg.get_type() == 'HEARTBEAT':
        print(msg)
        time.sleep(60)

'''