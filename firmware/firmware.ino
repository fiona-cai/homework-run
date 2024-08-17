#define left 5
#define middle 6
#define right 7

byte input;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(left, OUTPUT);
  pinMode(middle, OUTPUT);
  pinMode(right, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available() > 0) {
    input = Serial.read();
    switch(input) {
      case B00000001:
        digitalWrite(left, HIGH);
        break;
      case B00000010:
        digitalWrite(left, LOW);
        break;
      case B00000011:
        digitalWrite(middle, HIGH);
        break;
      case B00000100:
        digitalWrite(middle, LOW);
        break;
      case B00000101:
        digitalWrite(right, HIGH);
        break;
      case B00000110:
        digitalWrite(right, LOW);
        break;
    }
  }
}
