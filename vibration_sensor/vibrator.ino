int buzzerPin = 0;
const unsigned long duration = 500;
int key_received = 0;

void setup()
{
  Serial.begin(115200);
  Serial.setTimeout(1);
}

void vibrate(int pin)
{
  pinMode(pin, OUTPUT);
  unsigned long startTime = millis(); // Get the current time

  while (millis() - startTime < duration)
  {

    digitalWrite(pin, HIGH);
    delay(50);

    digitalWrite(pin, LOW);
    delay(50);
  }

  digitalWrite(pin, LOW);
}

void loop()
{
  while (!Serial.available())
    ;
  key_received = Serial.readString().toInt();

  switch (key_received)
  {
  case 1: // up
    buzzerPin = 9;
    Serial.print(key_received + 1);
    break;
  case 2: // right
    buzzerPin = 10;
    break;
  case 3: // down
    buzzerPin = 11;
    break;
  case 4: // left
    buzzerPin = 12;
    break;
  }
  vibrate(buzzerPin);
}
