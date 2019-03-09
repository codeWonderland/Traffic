import paho.mqtt.client as mqtt

conn = mqtt.Client(client_id="broker", clean_session="True", protocol=mqtt.MQTTv31, transport="tcp")
conn.connect("localhost")
conn.subscribe("traffic/lights")

conn.loop_forever()
