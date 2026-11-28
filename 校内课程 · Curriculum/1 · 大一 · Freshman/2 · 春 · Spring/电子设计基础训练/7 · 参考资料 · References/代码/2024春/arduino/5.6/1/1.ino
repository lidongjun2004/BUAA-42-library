#include "DHT.h"
#define DHTPIN 4
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);
void setup() {
  Serial.begin(9600);
  Serial.println(F("DHT11 test!"));dht.begin();

}

void loop() {
  // put your main code here, to run repeatedly:
  delay(2000);
  float i = millis();
  float h=dht.readHumidity();
  float t = dht.readTemperature();
  float j=millis();
  float k=j-i;
  Serial.print(F("Humidity: "));
  Serial.println(h);
  Serial.print(F("% Temperature: "));
  Serial.println(t);
}
