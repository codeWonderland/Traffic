import time

import paho.mqtt.client as mqtt

waiting = False


def on_message(client, userdata, message):
    global waiting

    data = str(message.payload.decode("utf-8")).upper()

    if data == 'N':
        print("Light facing N/S")

    elif data == 'W':
        print("Light facing E/W")

    else:
        print("NEW DATA TYPE: ", data)

    waiting = False


if __name__ == "__main__":
    conn = mqtt.Client(client_id="pub", clean_session="True", protocol=mqtt.MQTTv31, transport="tcp")

    conn.on_message = on_message

    conn.connect("localhost")
    conn.subscribe("traffic/pub")

    conn.loop_start()

    while True:
        if not waiting:
            command = input("What is your command (H for help)?").upper()[0]

            if command == 'H':
                print("help message")

            elif command == 'L':
                conn.publish("traffic/lights", command)

                waiting = True

            elif command in ['N', 'S', 'E', 'W']:
                conn.publish("traffic/lights", command)

            elif command == 'Q':
                break

        time.sleep(1)

    conn.loop_stop()
