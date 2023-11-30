from pymavlink import mavutil
import time

master = mavutil.mavlink_connection('tcp:127.0.0.1:5763')  #14550 for UDP

master.mav.request_data_stream_send(master.target_system, master.target_component,

                                        mavutil.mavlink.MAV_DATA_STREAM_RC_CHANNELS, 1, 1)

master.mav.param_set_send(
    master.target_system, master.target_component,
    b'SERVO2_FUNCTION',
    0,
    mavutil.mavlink.MAV_PARAM_TYPE_REAL32
)

master.mav.param_set_send(
    master.target_system, master.target_component,
    b'SERVO2_FUNCTION',
    19,
    mavutil.mavlink.MAV_PARAM_TYPE_REAL32
)
