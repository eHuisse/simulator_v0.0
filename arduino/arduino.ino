/*
  Blink

  Turns an LED on for one second, then off for one second, repeatedly.

  Most Arduinos have an on-board LED you can control. On the UNO, MEGA and ZERO
  it is attached to digital pin 13, on MKR1000 on pin 6. LED_BUILTIN is set to
  the correct LED pin independent of which board is used.
  If you want to know what pin the on-board LED is connected to on your Arduino
  model, check the Technical Specs of your board at:
  https://www.arduino.cc/en/Main/Products

  modified 8 May 2014
  by Scott Fitzgerald
  modified 2 Sep 2016
  by Arturo Guadalupi
  modified 8 Sep 2016
  by Colby Newman

  This example code is in the public domain.

  http://www.arduino.cc/en/Tutorial/Blink
*/
int RIGHT_PIN = 2;
int LEFT_PIN = 3;
int rightState = 0;
int leftState = 0;
bool toogleLed = 0;

String inputString = ""; 

// the setup function runs once when you press reset or power the board
void setup() {
  pinMode(RIGHT_PIN, INPUT);
  pinMode(LEFT_PIN, INPUT);
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(115200);
  // reserve 200 bytes for the inputString:
  inputString.reserve(200);
}

// the loop function runs over and over again forever
void loop() {
  rightState = digitalRead(RIGHT_PIN);
  leftState = digitalRead(LEFT_PIN);
  Serial.print(leftState);
  Serial.print(";");
  Serial.println(rightState);
  delay(10);        // delay in between reads for stability
  toogleLed =! toogleLed;
  digitalWrite(LED_BUILTIN, toogleLed);
}
