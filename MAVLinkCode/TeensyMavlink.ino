#include <MAVLink.h>

// Function to send a MAVLink message

//void sendNamedValueFloat(float value)
void send_AngleData_as_MAVLinkMessage(mavlink_channel_t channel, float angledata) // change to float values 
{
    
    mavlink_message_t msg;
    //mavlink_msg_your_message_pack(systemID, componentID, &msg,time_ms, value);  // Pack your data into the message // Note this is a custom message
    //mavlink_msg_named_value_float_pack(systemID, componentID, &msg, time_ms, "YourValueName", value);  // Pack your data into the message

    mavlink_msg_named_value_float_pack(0, 200, &msg, millis(), "AngleData", angledata); // here the specific standard mavlink ID is used ID: 251 for packing data into a named value float

    // Send the MAVLink message over the channel (e.g., Serial 5 on Teensy)

    //mavlink_msg_to_send_buffer(mavlink_get_channel_buffer(channel), &msg);  // encoding done here 
    //mavlink_transmit(channel, mavlink_get_channel_buffer(channel));

    uint8_t buf[MAVLINK_MAX_PACKET_LEN];
    uint16_t len = mavlink_msg_to_send_buffer(buf, &msg);

    // Send the MAVLink message over the serial port (Serial5 on Teensy)
    Serial5.write(buf, len);
}

void setup()
{
    Serial5.begin(57600);  // Set the baud rate to match your configuration
    
    int ledPin = 13;                 // LED connected to digital pin 13
    pinMode(ledPin, OUTPUT);      // sets the digital pin as output
}

void loop()
{
    // Your main loop code here

    // Example: Send a MAVLink message with data (replace with your actual data)
    float angledata = 42.0 ;//insert variable name from angle sensing code; // change to float values
    send_AngleData_as_MAVLinkMessage(MAVLINK_COMM_1, angledata);
    //int ledPin = 13
    //digitalWrite(13, HIGH);   // sets the LED on
    delay(1000);
    //digitalWrite(13, LOW);
    delay(1000);  // Adjust delay as needed
}


  

