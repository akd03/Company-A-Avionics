from pymavlink import mavutil
import time

master = mavutil.mavlink_connection('tcp:127.0.0.1:5763')  


def adjust_elevator(servo_number, pwm_value):

    master.mav.command_long_send(

        master.target_system, master.target_component,

        mavutil.mavlink.MAV_CMD_DO_SET_SERVO,

        0,

        servo_number,

        pwm_value,

        0, 0, 0, 0, 0 

    )


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


for us in range(1500, 1550, 10):
    adjust_elevator(2, us)
    time.sleep(0.125)
    msg2 = master.recv_match(type='SERVO_OUTPUT_RAW', blocking=True).to_dict()
    print(f"Servo 2: {msg2['servo2_raw']}")
    get_attitude()
    current_pitch, current_yaw, current_roll = get_attitude()
    print(f"Current Pitch: {current_pitch}, Current Yaw: {current_yaw}, Current Roll: {current_roll}")

for us in range(1550, 1400, -10):
    adjust_elevator(2, us)
    time.sleep(0.125)
    msg2 = master.recv_match(type='SERVO_OUTPUT_RAW', blocking=True).to_dict()
    print(f"Servo 2: {msg2['servo2_raw']}")
    get_attitude()
    current_pitch, current_yaw, current_roll = get_attitude()
    print(f"Current Pitch: {current_pitch}, Current Yaw: {current_yaw}, Current Roll: {current_roll}")


while True:
    msg = master.recv_match()
    if not msg:
        continue
    if msg.get_type() == 'HEARTBEAT':
        print(msg)
        time.sleep(60)
