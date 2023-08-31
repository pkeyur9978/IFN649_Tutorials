import paho.mqtt.publish as publish
publish.single("ifn649", "LED_ON", hostname="13.238.116.67") 
print("Done")
