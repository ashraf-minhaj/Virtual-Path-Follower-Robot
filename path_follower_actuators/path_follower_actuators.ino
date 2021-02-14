/* ** Virtual Path Following Robot *
 *  Robot Actuator's program
 *  
 *  This robot takes commands from a python program
 *  and follows those commands. This robot demonstrates
 *  virtual path following robots and it's scopes.
 *  
 *  *********** License: GPL3+  *************
 *  You should receive a copy of the license
 *  with this program.
 *  
 *  (c) author: ashraf minhaj
 *      mail  : ashraf_minhaj@yahoo.com
 *      
 *  Tutorial for this project:
 *      http://youtube.com/fusebatti
 *      http://ashrafminhajfb.blogspot.com
 *      
 *  written on 15th Feb 2021
 */

 // Declare motor pins
 // motors of same side work as one
 // so we can consider both as one.
int rightMotor1 = 2;                // right side
int rightMotor2 = 3;
int leftMotor1 = 5;                 // left side
int leftMotor2 = 6;

// Variable to store received data
byte command;

void setup() {
  // Set pin modes
  pinMode(rightMotor1, OUTPUT);
  pinMode(rightMotor2, OUTPUT);
  pinMode(leftMotor1, OUTPUT);
  pinMode(leftMotor2, OUTPUT);

  // Initialize serial communication
  // at 9600 buad rate
  // sender/python code will also use
  // the same buad
  Serial.begin(9600);
}

void loop() {
  // Get command data from bluetooth serial port
  command = Serial.read();

  // Decide which way to go based on received data
  if (command == 'f'){
    // indicates forward motion
    digitalWrite(rightMotor1, HIGH);
    digitalWrite(rightMotor2, LOW);
    digitalWrite(leftMotor1, HIGH);
    digitalWrite(leftMotor2, LOW);
  }

  if (command == 'b'){
    // Backward motion
    digitalWrite(rightMotor1, LOW);
    digitalWrite(rightMotor2, HIGH);
    digitalWrite(leftMotor1, LOW);
    digitalWrite(leftMotor2, HIGH);
  }

  if (command == 'r'){
    // Right turn
    digitalWrite(rightMotor1, LOW);
    digitalWrite(rightMotor2, HIGH);
    digitalWrite(leftMotor1, HIGH);
    digitalWrite(leftMotor2, LOW);
  }

  if (command == 'l'){
    // Left turn
    digitalWrite(rightMotor1, HIGH);
    digitalWrite(rightMotor2, LOW);
    digitalWrite(leftMotor1, LOW);
    digitalWrite(leftMotor2, HIGH);
  }

  if (command == 's'){
    // Stops the robot/car
    digitalWrite(rightMotor1, LOW);
    digitalWrite(rightMotor2, LOW);
    digitalWrite(leftMotor1, LOW);
    digitalWrite(leftMotor2, LOW);
  }
}
