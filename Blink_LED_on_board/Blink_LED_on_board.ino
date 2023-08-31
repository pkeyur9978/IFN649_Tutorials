// This program blinks an external LED connected to pin 17 of the Teensy board.
// The LED will turn ON for 3 seconds and then OFF for 3 seconds.

const int ledPin = 17;  // Define the pin where the LED is connected

void setup() {
  pinMode(ledPin, OUTPUT);  // Set the LED pin as an output
}

void loop() {
  digitalWrite(ledPin, HIGH);  // Turn the LED ON
  delay(3000);                 // Wait for 3 seconds
  digitalWrite(ledPin, LOW);   // Turn the LED OFF
  delay(3000);                 // Wait for 3 seconds
}
