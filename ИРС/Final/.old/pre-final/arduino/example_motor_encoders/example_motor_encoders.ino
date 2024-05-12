#include "Motor.h"

#define DM1 32
#define SM1 4
#define E1M1 12
#define E2M1 17

#define DM2 18
#define SM2 19
#define E1M2 14
#define E2M2 26

Motor M1(DM1, SM1, E1M1, E2M1, 5);
Motor M2(DM2, SM2, E1M2, E2M2, 0);

void attachMotors() {
  attachInterrupt(M1.e1Port, M1.updateEncoder, CHANGE);
  attachInterrupt(M1.e2Port, M1.updateEncoder, CHANGE);
  attachInterrupt(M2.e1Port, M2.updateEncoder, CHANGE);
  attachInterrupt(M2.e2Port, M2.updateEncoder, CHANGE);
}

void reset() {
  M1.resetEncoder();
  M2.resetEncoder();
}

void stop() {
  M1.setSpeed(0);
  M2.setSpeed(0);
}

void forwardTime(int speed, int time) {
  M1.run(FORWARD);
  M2.run(FORWARD);
  M1.setSpeed(speed);
  M2.setSpeed(speed);
  delay(time);
  stop();
}

void forward(int speed, int dist) {
  reset();
  M1.run(FORWARD);
  M2.run(FORWARD);
  M1.setSpeed(speed);
  M2.setSpeed(speed);
  while ((M1.getEncoder() + M2.getEncoder()) < dist) {}
  stop();
}

void backwardTime(int speed, int time) {
  M1.run(BACKWARD);
  M2.run(BACKWARD);
  M1.setSpeed(speed);
  M2.setSpeed(speed);
  delay(time);
  stop();
}

void backward(int speed, int dist) {
  reset();
  M1.run(BACKWARD);
  M2.run(BACKWARD);
  M1.setSpeed(speed);
  M2.setSpeed(speed);
  while ((abs(M1.getEncoder()) + abs(M2.getEncoder())) < dist) {}
  stop();
}

void rightTime(int speed, int time) {
  M1.run(BACKWARD);
  M2.run(FORWARD);
  M1.setSpeed(speed);
  M2.setSpeed(speed);
  delay(time);
  stop();
}

void right(int speed, int dist) {
  reset();
  M1.run(BACKWARD);
  M2.run(FORWARD);
  M1.setSpeed(speed);
  M2.setSpeed(speed);
  while (abs(M2.getEncoder()) < dist) {}
  stop();
}

void leftTime(int speed, int time) {
  M1.run(FORWARD);
  M2.run(BACKWARD);
  M1.setSpeed(speed);
  M2.setSpeed(speed);
  delay(time);
  stop();
}

void left(int speed, int dist) {
  reset();
  M1.run(FORWARD);
  M2.run(BACKWARD);
  M1.setSpeed(speed);
  M2.setSpeed(speed);
  while (abs(M1.getEncoder()) < dist) {}
  stop();
}

void setup() {
  attachMotors();
}

void loop() {
}
