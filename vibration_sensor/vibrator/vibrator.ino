int buzzerPin = 0;  
const unsigned long duration = 500; 
int key_received=0;

void setup() {
  //pinMode(buzzerPin, OUTPUT);  
  Serial.begin(9600);
  Serial.setTimeout(0.05);
 
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
  //vibrate(12);
  
  while (!Serial.available());
  key_received = Serial.readString().toInt();
  //if (Serial.available() >= 2) {
  // received_key = Serial.read() + (Serial.read() << 8);
  
  switch (key_received){
     case 1: //up
       buzzerPin=13;
       Serial.print(key_received);
       break;
     case 2: //right
       buzzerPin=12;
       Serial.print(key_received);
       break;
     case 3: //down
       buzzerPin=7;
       Serial.print(key_received);
       break;
     case 4: //left
       buzzerPin=8;
       Serial.print(key_received);
       break;
   }
   vibrate(buzzerPin);
}
