import re
import paho.mqtt.client as mqtt

# Configure the MQTT broker and topic
mqtt_broker = "13.54.15.49"
mqtt_port = 1883
mqtt_topic = "sensor_data/all"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(mqtt_topic)

def on_message(client, userdata, message):
    # Callback when a message is received
    data = message.payload.decode()
    print(f'Received data: {data}')

    # Extract temperature value
    temperature_match = re.search(r"Temperature:\s+(\d+\.\d+)", data)
    if temperature_match:
        temperature = float(temperature_match.group(1))
        print(f"Extracted temperature: {temperature}°C")

    # Extract humidity value
    humidity_match = re.search(r"Humidity:\s+(\d+\.\d+)", data)
    if humidity_match:
        humidity = float(humidity_match.group(1))
        print(f"Extracted humidity: {humidity}%")

    # Extract soil moisture value
    soil_moisture_match = re.search(r"Soil Moisture:\s+(\d+\.\d+)", data)
    if soil_moisture_match:
        soil_moisture = float(soil_moisture_match.group(1))
        print(f"Extracted soil moisture: {soil_moisture}%")

# Create and configure the MQTT client
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Connect to the MQTT broker and start the loop
mqtt_client.connect(mqtt_broker, mqtt_port, 60)
mqtt_client.loop_start()

try:
    # Keep the script running
    while True:
        # You can do other tasks here
        pass
except KeyboardInterrupt:
    print("Exiting gracefully")
    # Stop the loop before finishing
    mqtt_client.loop_stop()
