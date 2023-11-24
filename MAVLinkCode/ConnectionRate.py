from pymavlink import mavutil
import math
import time


conn = mavutil.mavlink_connection("com14") # com7
conn.wait_heartbeat()


# mavlink message id must be set for faster communication !!!!
# message speed must be set per message as of 24/11 not found a way to do for multiple messages at once

m = conn.mav.command_long_encode(
        conn.target_system, conn.target_component,
        511, 0,
        33, # The MAVLink message ID
        30000, # The interval between two messages in microseconds. Set to -1 to disable and 0 to request default rate.
        0, 
        0, 
        0, 
        0, # Unused parameters
        0, # Target address of message stream - 0 default
    )

conn.mav.send(m)
print("CONNECTED!")


start=time.time()
hz_list = [0]
while True:
    # Important section below, make sure message id "33" is the same as the message you are recieving "GLOBAL_POSITION_INT"
    ######################################################################################
    conn.mav.request_data_stream_send(conn.target_system, conn.target_component,
                                        33, 10, 1)
    m = conn.recv_match(type="GLOBAL_POSITION_INT", blocking=True)
    ######################################################################################

    if m is not None: # calculating frequency of recieved messages
        now = time.time()
        hz_list.append(now-start)
        start = now
        print(f"{round(1/(sum(hz_list)/len(hz_list)), 3)}Hz")
    
        
