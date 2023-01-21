"""
MQTT Smart Sensor 2

Created by: Ayoub OUARKA 
Email     : ouarka.dev@gmail.com 

"""
import time
import requests
import paho.mqtt.client as mqtt
import random 
import json

API_URL = "http://192.168.43.147:5000/predict"

# let's connect to the MQTT broker
MQTT_BROKER_URL    = "localhost"
MQTT_PUBLISH_TOPIC = "equip_2" #equipement 1


mqttc = mqtt.Client()
mqttc.connect(MQTT_BROKER_URL)


# Infinite loop of fake data sent to the Broker
while True:
    # air_temp = fake.random_int(min=296.0, max=305.0)
    # process_temp = fake.random_float(min=306.0,max=314.0)

    t = {
        'air_temp': round(random.uniform(296.0, 305.0), 3), 
        'process_temp': round(random.uniform(305.0, 314.0), 3),
        'rotational_speed':random.randint(1168, 2886),
        'torque' :round(random.uniform(3.8, 76.6),2),
        'tool_wear': random.randint(52, 253)
    }

    # send request to api for prediction 
    resp = requests.post(API_URL, json=t)

    if resp.status_code == 200:
      o = resp.json()
      t['failure_pred'] = o['pred']
    else :
      t['failure_pred'] = -1
    


    # print(json.dumps(t))
    mqttc.publish(MQTT_PUBLISH_TOPIC, json.dumps(t))
    print(f"Published equip 2: {json.dumps(t)}")

    # sleep for 1min
    time.sleep(60)