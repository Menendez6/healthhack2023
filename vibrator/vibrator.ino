int buzzerPin = 0;  
const unsigned long duration = 1000; 
int key_received=0;

void setup() {
  //pinMode(buzzerPin, OUTPUT);  
  Serial.begin(115200);
  Serial.setTimeout(1);
 
}

void vibrate(int pin){
  pinMode(pin, OUTPUT);
  unsigned long startTime = millis();  // Get the current time

  //Serial.print(x + 2);
  while (millis() - startTime < duration) {
    
    digitalWrite(pin, HIGH);
    delay(50); 

   
    digitalWrite(pin, LOW);
    delay(50);  
  }
  
 
  digitalWrite(pin, LOW);
  
  
}


void loop() {
  while (!Serial.available());
  key_received = Serial.readString().toInt();
  //if (Serial.available() >= 2) {
  // received_key = Serial.read() + (Serial.read() << 8);
  
  switch (key_received){
     case 1:
       buzzerPin=9;
       Serial.print(key_received + 1);
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
   }
   vibrate(buzzerPin);
}
