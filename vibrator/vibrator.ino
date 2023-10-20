int buzzerPin = 0;  
const unsigned long duration = 1000; 
uint_16 received_key=0;

void setup() {
  pinMode(buzzerPin, OUTPUT);  
  Serial.begin(115200);
 
}

void vibrate(uint_16 pin){
  unsigned long startTime = millis();  // Get the current time

  
  while (millis() - startTime < duration) {
    
    digitalWrite(pin, HIGH);
    delay(50); 

   
    digitalWrite(pin, LOW);
    delay(50);  
  }
  
 
  digitalWrite(pin, LOW);
  
  
}


void loop() {
  if (Serial.available() >= 2) {
   received_key = Serial.read() + (Serial.read() << 8);
   switch (key) {
     case 1:
       buzzerPin=9;
       break;
     case 2:
       buzzerPin=10;
       break;
     case 3:
       buzzerPin=11;
       break;
     case 4:
       buzzerPin=12;
       break;
   vibrate(buzzerPin);
   
}
