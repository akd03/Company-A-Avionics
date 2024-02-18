#include <Wire.h>
#include <MAVLink.h>

float RatePitch;
float AnglePitch = 0; //This is for Accelerometer.
float AnglePitch1 = 0;  //This is for Gyroscope.
float AccX, AccY, AccZ; //Accelerometer values, I put some redundant axis in case the sensor orientation has to be changed.
float rad_to_deg = 180 / 3.141592654;


bool systemIsStationary() {
  return abs(AnglePitch1) <= 0.5;
} // precision to 0.5 degrees, also determining if the UAV is stable

int sensorValue2 = 0;
int outputValue2 = 0;

unsigned long previousTime = 0; //time in milli sec is going to be verylong, positive value,
unsigned long previousTime2 = 0;
float gyroBiasPitch = 0;
float alpha = 0.95;  // Complementary filter coefficient

void gyro_signals(void) {

  Wire.beginTransmission(0x68);
  Wire.write(0x43); //Readings from the Gyro data registers
  Wire.endTransmission(false);
  Wire.requestFrom(0x68, 6, true); // Read 6 bytes data from the slave, MPU6050

  int16_t GyroY = Wire.read() << 8 | Wire.read();  //If sensor orientations change, swap X and Y accordingly.
  int16_t GyroX = Wire.read() << 8 | Wire.read();  
  int16_t GyroZ = Wire.read() << 8 | Wire.read();

  RatePitch = (float)GyroY / 65.5 - gyroBiasPitch;

  Wire.beginTransmission(0x68);
  Wire.write(0x3B); //Reading from the Accelerometer data registers
  Wire.endTransmission(false);
  Wire.requestFrom(0x68, 6, true); 

  int16_t AccXLSB = Wire.read() << 8 | Wire.read();  
  int16_t AccYLSB = Wire.read() << 8 | Wire.read();  
  int16_t AccZLSB = Wire.read() << 8 | Wire.read();

  AccX = (float)AccXLSB / 16384.0;  //Raw sensor values, divide it by some constant( in this case 16384 which is the full sensitivity), to normalise the values (sort of like filtering and stuffs)
  AccY = (float)AccYLSB / 16384.0;
  AccZ = (float)AccZLSB / 16384.0;

  // Integrate gyro rate to get pitch angle
  unsigned long currentTime = millis();
  float deltaTime = (currentTime - previousTime) / 1000.0;
  AnglePitch += RatePitch * deltaTime;  //integration method

  AnglePitch1 = -atan(AccY / sqrt(AccX * AccX + AccZ * AccZ)) * (180 / 3.141592);  //This method is converting the Acceleration vectors and calculate the vector angles (offset from 0point), mathematically AND practically very accurate 

  // Apply complementary filter, FilteredAngle = α × (GyroscopeAngle + GyroscopeBias) + (1−α) × AccelerometerAngle
  AnglePitch = alpha * (AnglePitch + RatePitch * deltaTime) + (1 - alpha) * AnglePitch1;   

  previousTime = currentTime; //return to the start for next delta T
}

void calibrateGyro() {
  for (int i = 0; i < 1000; i++) {
    gyro_signals();  //calling a fuction that will run in the set up,
    gyroBiasPitch += RatePitch; //pitch rate updates the gyroscope bias (callibration)
    delay(1); //don't touch zis!!
  }

  gyroBiasPitch /= 1000; //averaging the bias since the delay is 1 mili sec
}

void setup() {

  Serial.begin(57600);
  pinMode(13, OUTPUT);
  digitalWrite(13, HIGH);
  
  Wire.begin();
  Wire.setClock(400000);
  Wire.begin();
  //delay(100); // don't touch this.

  Wire.beginTransmission(0x68);
  Wire.write(0x6B);
  Wire.write(0x00);
  Wire.endTransmission(true);

  calibrateGyro();  // Calibrate gyro during setup

  // Print initial value for Serial Plotter
  Serial.print(0);
  Serial.print(" "); //space
  Serial.println(0);
}

void loop() {
  
  gyro_signals();
  Serial.print(-90);        //To freeze the lower limit
  Serial.print(" ");
  Serial.print(90);       //To freeze the upper limit
  Serial.print(" ");


  float elevator_angle = AnglePitch1;

  mavlink_message_t msg;

  uint8_t buf[MAVLINK_MAX_PACKET_LEN];

  //Packing NAMED_VALUE_FLOAT message

  mavlink_msg_named_value_float_pack(0, 200, &msg, millis(), "ElevatorAngle", elevator_angle);
  uint16_t len = mavlink_msg_to_send_buffer(buf, &msg);
  Serial.write(buf, len);
  


  //Print values for Serial Plotter
  Serial.println(AnglePitch1);
  delay(100);
    //do not adjust the delay time unless you have calculated the time dependencies
}



