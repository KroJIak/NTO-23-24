#include "Motor.h"

Motor M1(19, 18);
Motor M2(4, 32);

void setup() {
  M1.run(RELEASE);
  M2.run(RELEASE);
  Serial.begin(9600);
}

void loop() {
  M1.run(FORWARD);
  M2.run(FORWARD);
  delay(5000);
  M1.run(BACKWARD);
  M2.run(BACKWARD);
}
