char x=0;
void setup()
{ 
Serial.begin(9600); //波特率9600
}
void loop()
{
  if(Serial.available()>0)
   {  
      x=Serial.read();
      Serial.print("I have received:"); 
      Serial.println(x);  //输出并换行
   }
  delay(200);
}
