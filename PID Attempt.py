from pymavlink import mavutil
import time

master = mavutil.mavlink_connection('tcp:127.0.0.1:5762')  

def get_attitude():

    master.mav.request_data_stream_send(master.target_system, master.target_component,

                                        mavutil.mavlink.MAV_DATA_STREAM_EXTENDED_STATUS, 1, 1)

    msg = master.recv_match(type='ATTITUDE', blocking=True)

    if msg:

        return msg.pitch, msg.yaw, msg.roll

    else:

        return None, None, None

servo_number = 2

def adjust_flap(servo_number, pwm_value):

    master.mav.command_long_send(

        master.target_system, master.target_component,

        mavutil.mavlink.MAV_CMD_DO_SET_SERVO,

        0,

        servo_number,

        pwm_value,

        0, 0, 0, 0, 0 

    )

 

try:

    desired_pitch = float(input("What pitch angle do you need? "))

    while True:

        current_pitch, _, _ = get_attitude()

        if current_pitch != desired_pitch:

            print(f"Current Pitch: {current_pitch}, Desired Pitch: {desired_pitch}")

            pwm_value = (desired_pitch - current_pitch) * 100 

            pwm_value = max(1000, min(2000, pwm_value)) 

            adjust_flap(1, pwm_value)

        time.sleep(0.02) 

 

except ValueError:

    print("Invalid input for pitch angle.")

while True:
    msg = master.recv_match()
    if not msg:
        continue
    if msg.get_type() == 'HEARTBEAT':
        print(msg)
        time.sleep(60)