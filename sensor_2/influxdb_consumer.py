"""
MQTT subscriber - Listen to a topic and sends data to InfluxDB
"""

import os
from dotenv import load_dotenv
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import ASYNCHRONOUS, SYNCHRONOUS
import paho.mqtt.client as mqtt
import time
import json

load_dotenv()  # take environment variables from .env.

# InfluxDB config
BUCKET = os.getenv('INFLUXDB_BUCKET')

client = InfluxDBClient(url=os.getenv('INFLUXDB_URL'),
                token=os.getenv('INFLUXDB_TOKEN'), org=os.getenv('INFLUXDB_ORG'), debug=False)
write_api = client.write_api()


MQTT_BROKER_URL    = "localhost"
MQTT_PUBLISH_TOPIC = "equip_2"


mqttc = mqtt.Client()
mqttc.connect(MQTT_BROKER_URL)

def on_connect(client, userdata, flags, rc):
    """ The callback for when the client connects to the broker."""
    print("Connected with result code "+str(rc))

    # Subscribe to a topic
    client.subscribe(MQTT_PUBLISH_TOPIC)

def on_message(client, userdata, msg):
    """ The callback for when a PUBLISH message is received from the server."""

    # We received bytes we need to convert into something usable
    t = json.loads(msg.payload)


    ## InfluxDB logic
    point = Point(MQTT_PUBLISH_TOPIC)
    for key, value in t.items(): 
        print(key, value)
        point.field(key, value)
        
    point.time(int(time.time_ns()))
    write_api.write(bucket=BUCKET, record=point)

## MQTT logic - Register callbacks and start MQTT client
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.loop_forever()


