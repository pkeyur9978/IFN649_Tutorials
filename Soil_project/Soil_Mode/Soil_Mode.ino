#include "DHT.h"
#include "DHT_U.h"

#define DHTPIN 21
#define DHTTYPE DHT11
#define SOIL_SENSOR_PIN 10
#define LED_LOW 3
#define LED_MEDIUM 4
#define LED_HIGH 5

DHT dht(DHTPIN, DHTTYPE);

int moistureValue;
float moisturePercentage;

void setup() {
  Serial.begin(9600);
  dht.begin();
  pinMode(DHTPIN, INPUT);
  pinMode(SOIL_SENSOR_PIN, INPUT);
  pinMode(LED_LOW, OUTPUT);
  pinMode(LED_MEDIUM, OUTPUT);
  pinMode(LED_HIGH, OUTPUT);
}

void loop() {
  float h = dht.readHumidity();
  float t = dht.readTemperature();

  moistureValue = analogRead(SOIL_SENSOR_PIN);
  moisturePercentage = (moistureValue / 539.00) * 100;

  Serial.print("Temperature: "); Serial.print(t);
  Serial.print(" Humidity: "); Serial.print(h);
  Serial.print(" Soil Moisture: "); Serial.print(moisturePercentage); Serial.println("%");

  if (moisturePercentage < 30) {  // Assuming <30% is low
    digitalWrite(LED_LOW, HIGH);
    digitalWrite(LED_MEDIUM, LOW);
    digitalWrite(LED_HIGH, LOW);
  } else if (moisturePercentage >= 30 && moisturePercentage < 70) {  // Assuming 30-70% is medium
    digitalWrite(LED_LOW, LOW);
    digitalWrite(LED_MEDIUM, HIGH);
    digitalWrite(LED_HIGH, LOW);
  } else {
    digitalWrite(LED_LOW, LOW);
    digitalWrite(LED_MEDIUM, LOW);
    digitalWrite(LED_HIGH, HIGH);
  }

  delay(2000);
}