import paho.mqtt.client as mqtt
import serial 
def on_connect(client, userdata, flags, rc): 
	# func for making connection print("Connected to MQTT")
	print("Connection returned result: " + str(rc) )
	client.subscribe("ifn649")
def on_message(client, userdata, msg): 
	print(msg.topic+" "+str(msg.payload))
	ser.write(str.encode(msg))
	
client = mqtt.Client() 
client.on_connect = on_connect 
client.on_message = on_message
client.connect("13.238.116.67", 1883, 60) 
ser = serial.Serial("/dev/rfcomm0",9600)
client.loop_forever()