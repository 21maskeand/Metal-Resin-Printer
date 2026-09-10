#include <AccelStepper.h>
#include <AccelStepperWithDistance.h>

const int m0Pin = 9;
const int m1Pin = 10;
const int m2Pin = 11;

const int stepsPerRev = 200;
const int microStep = 32;
const int pitch = 4;

const int stepPin = 19;
const int dirPin = 18;

AccelStepperWithDistance stepper(AccelStepperWithDistance::DRIVER , stepPin , dirPin);


void setup() {
  // put your setup code here, to run once:

  Serial.begin(9600);

  // Sets microstepping mode to 32 microsteps per step.
  pinMode(m0Pin , OUTPUT);
  pinMode(m1Pin , OUTPUT);
  pinMode(m2Pin , OUTPUT);

  digitalWrite(m0Pin , HIGH);
  digitalWrite(m1Pin , HIGH);
  digitalWrite(m2Pin , HIGH);

//  digitalWrite(m0Pin , LOW);
//  digitalWrite(m1Pin , LOW);
//  digitalWrite(m2Pin , LOW);

  stepper.setMaxSpeed(4000);
  stepper.setAcceleration(2000);
  stepper.setStepsPerRotation(stepsPerRev);
  stepper.setMicroStep(microStep);
  stepper.setDistancePerRotation(pitch);
  stepper.setMinPulseWidth(5);   // microseconds



  //Serial.println("Starting Moving Up");
  stepper.runToNewDistance(10);
 // Serial.println("Done Moving Up");
  delay(1000);
 // Serial.println("Starting Moving Down");
  stepper.runToNewDistance(0);
  //Serial.println("Done Moving Down");
  delay(1000);


}

void loop() {



}
