const int stepPin = 19, dirPin = 18;
const int m0Pin = 9, m1Pin = 10, m2Pin = 11;

void setup() {
  pinMode(m0Pin, OUTPUT); pinMode(m1Pin, OUTPUT); pinMode(m2Pin, OUTPUT);
  digitalWrite(m0Pin, HIGH); digitalWrite(m1Pin, HIGH); digitalWrite(m2Pin, HIGH);
  pinMode(stepPin, OUTPUT); pinMode(dirPin, OUTPUT);
  digitalWrite(dirPin, HIGH);
}

void loop() {
  digitalWrite(stepPin, HIGH); delayMicroseconds(500);
  digitalWrite(stepPin, LOW);  delayMicroseconds(500);
}