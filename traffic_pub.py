import paho.mqtt.client as mqtt
import random
import time

conn = mqtt.Client(client_id="pub", clean_session="True",  protocol=mqtt.MQTTv31, transport="tcp")
conn.connect("localhost")
DIRS = ["east", "west"]

while True:
    conn.publish("traffic/lights", random.choice(DIRS))
    time.sleep(2)
