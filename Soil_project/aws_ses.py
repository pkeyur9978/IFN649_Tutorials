import paho.mqtt.client as mqtt
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re

# MQTT configuration
mqtt_broker = "13.54.15.49"
mqtt_port = 1883
mqtt_topic = "sensor_data/all"

# AWS SES configuration
aws_ses_smtp_username = "AKIAXMLKQIQLNSG2EZGV"
aws_ses_smtp_password = "BIQKM8psZm0wj/qg5jp5Ppgjh2zaw5oQje6uLgxcKeif"
aws_ses_region = "ap-southeast-2"  # Adjust to your AWS region
sender_email = "pkeyur9978@gmail.com"
recipient_email = "pkeyur1929@gmail.com"

# Thresholds for alerts
temperature_threshold = 20.0
humidity_low_threshold = 20.0
humidity_high_threshold = 35.0
soil_moisture_threshold = 30

def send_email(subject, message):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    body = message
    msg.attach(MIMEText(body, 'plain'))

    try:
        ses_client = smtplib.SMTP('email-smtp.' + aws_ses_region + '.amazonaws.com', 587)
        ses_client.starttls()
        ses_client.login(aws_ses_smtp_username, aws_ses_smtp_password)
        ses_client.sendmail(sender_email, recipient_email, msg.as_string())
        ses_client.quit()
        print("Email sent successfully")
    except Exception as e:
        print("Email could not be sent:", e)

def on_message(client, userdata, message):
    data = message.payload.decode()
    print("Received data:", data)

    # Extract temperature, humidity, and soil moisture values
    temperature_match = re.search(r"Temperature:\s+(\d+\.\d+)", data)
    humidity_match = re.search(r"Humidity:\s+(\d+\.\d+)", data)
    soil_moisture_match = re.search(r"Soil Moisture:\s+(\d+)", data)

    if temperature_match:
        temperature = float(temperature_match.group(1))
        print("Extracted temperature:", temperature)
        if temperature > temperature_threshold:
            alert_message = f"Temperature alert: {temperature}°C exceeds the threshold of {temperature_threshold}°C."
            send_email("Temperature Alert", alert_message)

    if humidity_match:
        humidity = float(humidity_match.group(1))
        print("Extracted humidity:", humidity)
        if humidity < humidity_low_threshold:
            alert_message = f"Humidity alert: {humidity}% is below the minimum threshold of {humidity_low_threshold}%."
            send_email("Low Humidity Alert", alert_message)
        elif humidity > humidity_high_threshold:
            alert_message = f"Humidity alert: {humidity}% exceeds the maximum threshold of {humidity_high_threshold}%."
            alert_message = f"Humidity alert: {humidity}% exceeds the maximum threshold of {humidity_high_threshold}%."
            send_email("High Humidity Alert", alert_message)

    if soil_moisture_match:
        soil_moisture = int(soil_moisture_match.group(1))
        print("Extracted soil moisture:", soil_moisture)
        if soil_moisture < soil_moisture_threshold:
            alert_message = f"Soil moisture alert: {soil_moisture}% is below the threshold of {soil_moisture_threshold}%. Consider watering the plants."
            send_email("Soil Moisture Alert", alert_message)

def on_connection(client, udata, flags, rc):
    print("Connected to MQTT broker")
    mqtt_client.subscribe(mqtt_topic)

# Configure the MQTT client
mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message
mqtt_client.on_connect = on_connection
mqtt_client.connect(mqtt_broker, mqtt_port)
mqtt_client.loop_start()

try:
    while True:
        pass
except KeyboardInterrupt:
    print("Exiting...")
