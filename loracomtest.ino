#include "LDHT.h"

#define DHTPIN 7          // what pin we're connected to
#define DHTTYPE DHT22     // using DHT22 sensor

LDHT dht(DHTPIN, DHTTYPE);

float tempC = 0.0, Humi = 0.0;
char readcharbuffer[20];
int readbuffersize;
char temp_input;

void setup(){

  Serial.begin(9600);
  Serial1.begin(9600);

	dht.begin();

	Serial.print(DHTTYPE);
	Serial.println(" test!");
}
void loop(){

	if (dht.read())
	{
		tempC = dht.readTemperature();
		Humi = dht.readHumidity();


		Serial.println("------------------------------");
		Serial.print("Temperature Celcius = ");
		Serial.print(dht.readTemperature());
		Serial.println("C");

		Serial.print("Temperature Fahrenheit = ");
		Serial.print(dht.readTemperature(false));
		Serial.println("F");

		Serial.print("Humidity = ");
		Serial.print(dht.readHumidity());
		Serial.println("%");

		Serial.print("HeatIndex = ");
		Serial.print(dht.readHeatIndex(tempC, Humi));
		Serial.println("C");

		Serial.print("DewPoint = ");
		Serial.print(dht.readDewPoint(tempC, Humi));
		Serial.println("C");

		Serial.println("Ready to Send");
		Serial.print("AT+DTX=11,\"T");
		Serial.print(dht.readHeatIndex(tempC, Humi));
		Serial.print(dht.readHumidity());
		Serial.println("\"");

		Serial1.print("AT+DTX=11,\"T");
		Serial1.print(dht.readHeatIndex(tempC, Humi));
		Serial1.print(dht.readHumidity());
		Serial1.println("\"");

		//Serial1.println("AT+DTX=11,\"12345ABCdef\"");
	}

  if(Serial1.read()){
    Serial.print(Serial1.read());
    Serial1.print("AT+DRX?");
  }
  
	delay(1000);

	/*
  Serial.println("Ready to Send");
  Serial1.println("AT+DTX=11,\"12345ABCdef\"");
  delay(1000);*/
  readbuffersize = Serial1.available();
  while(readbuffersize){
    temp_input = Serial1.read();
    Serial.print(temp_input);
    readbuffersize--;
 }
 delay(9000);
   readbuffersize = Serial1.available();
  while(readbuffersize){
    temp_input = Serial1.read();
    Serial.print(temp_input);
    readbuffersize--;
 }
 Serial.println("things");
  delay(10000);
}
