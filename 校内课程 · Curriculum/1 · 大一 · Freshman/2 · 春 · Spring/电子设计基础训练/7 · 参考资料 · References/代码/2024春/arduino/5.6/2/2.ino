#include <Adafruit_TCS34725.h>
#include <Wire.h>
Adafruit_TCS34725 tcs = Adafruit_TCS34725(TCS34725_INTEGRATIONTIME_50MS,TCS34725_GAIN_4X);
void setup() {
  // put your setup code here, to run once:

  Serial.begin(9600);
  if (tcs.begin()) 
  { 
    Serial.println("Found sensor");
  }
  else 
  {
    Serial.println("No TCS34725 found ... check your connections");
    
  }
  tcs.setInterrupt(true);
}

void loop() {
  // put your main code here, to run repeatedly:
  uint16_t clear, red, green, blue;
  tcs.getRawData(&red, &green, &blue, &clear);
  uint32_t sum = clear;
  float r, g, b;
  r = red; r /= sum;
  g = green; g /= sum;
  b = blue; b /= sum;
  r *= 256; g *= 256; b *= 256;
  Serial.print("red:"); Serial.println((int)r);
  Serial.print("green:"); Serial.println((int)g);
  Serial.print("blue:"); Serial.println((int)b);
  delay(1000);
}
