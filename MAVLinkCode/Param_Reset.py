from pymavlink import mavutil
import time

master = mavutil.mavlink_connection('tcp:127.0.0.1:5763')  #14550 for UDP

master.mav.request_data_stream_send(master.target_system, master.target_component,

                                        mavutil.mavlink.MAV_DATA_STREAM_RC_CHANNELS, 1, 1)


master.mav.param_set_send(
    master.target_system, master.target_component,
    b'SERVO2_FUNCTION',
    19,
    mavutil.mavlink.MAV_PARAM_TYPE_REAL32
)

master.mav.param_set_send(
    master.target_system, master.target_component,
    b'SERVO1_FUNCTION',
    4,
    mavutil.mavlink.MAV_PARAM_TYPE_REAL32
)

master.mav.param_set_send(
    master.target_system, master.target_component,
    b'SERVO4_FUNCTION',
    21,
    mavutil.mavlink.MAV_PARAM_TYPE_REAL32
)

response = master.recv_match(type='COMMAND_ACK', blocking=True)
if response and response.command == mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL and response.result == mavutil.mavlink.MAV_RESULT_ACCEPTED:
    print("Command accepted")
else:
    print("Command failed")
    quit()
