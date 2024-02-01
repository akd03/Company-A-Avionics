'''
Created by Gabriel Gekonge on 31/01/2024

This is data stream between Cube and Teensy using respective serial libraries

An alternative to this is mavlink implementation which is currently in development as of 01/02/2024

'''

while True:

    '''

    while True means that the block of code inside the loop will be executed indefinitely 
    until the loop is explicitly broken.

    '''

#Receive / read message / data from telem 2 on cube orange
    
    ser_cube = serial.Serial('COM10', 57600)  # Adjust baud rate as needed

    '''

ser_cube is a variable that is being assigned an instance of the Serial class from the serial library.

57600 is the baud rate, which specifies the speed of communication between the devices.

'''

## Check if data is available on the serial port
    
    if ser_cube.in_waiting > 0:

        data = ser_cube.readline().decode('utf-8').strip()
        
        try:
            # Convert the received string to float
            angle = float(data)

            print(f"Received angle data from teensy {angle}")

        except ValueError:
            print(f"Invalid data received: {data}")        
        
        
