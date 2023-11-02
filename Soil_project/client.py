import paho.mqtt.client as mqtt
import serial
import time
import paho.mqtt.publish as publish

# Configure the MQTT broker and topic
mqtt_broker = "13.54.15.49"
mqtt_port = 1883
mqtt_topic = "sensor_data/all"

# Configure the serial communication
ser = serial.Serial("/dev/rfcomm0", 9600)
ser.write(str.encode('Start\r\n'))

# Callback when a message is received from the MQTT broker
def on_message(client, userdata, message):
	
    data = message.payload.decode()
    print(data)

def on_connection(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(mqtt_topic)

# Configure the MQTT client
mqtt_client = mqtt.Client()

try:
    mqtt_client.on_message = on_message
    mqtt_client.on_connect = on_connection
    mqtt_client.connect(mqtt_broker, mqtt_port)
    mqtt_client.loop_start()

    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            print(line)
            
            # Assuming that the microcontroller sends data in the format:
            # "Temperature: xx.x Humidity: xx.x Soil Moisture: xx.x%"
            # Adjust if necessary based on the actual data format.
            
            try:
                # Publishing the raw line data to the MQTT topic
                publish.single(mqtt_topic, line, hostname=mqtt_broker)

            except ValueError:
                print("Error parsing sensor data: ", line)

            time.sleep(2)
except KeyboardInterrupt:
    print("Exiting...")
    mqtt_client.loop_stop()
    ser.close()
except serial.SerialException:
    print("Serial connection error")
except Exception as e:
    print("An error occurred: ", str(e))
