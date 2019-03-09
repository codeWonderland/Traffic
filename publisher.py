import time

import paho.mqtt.client as mqtt

waiting = False
auth_status = False
lights_topic = "traffic/auth"


def on_message(client, userdata, message):
    global waiting
    global lights_topic
    global auth_status

    data = str(message.payload.decode("utf-8")).upper()

    if data == 'N':
        print("Light facing N/S")

        waiting = False

    elif data == 'W':
        print("Light facing E/W")

        waiting = False

    elif data.__contains__('/') and auth_status is False:
        lights_topic = data.lower()

        auth_status = True

    else:
        print("NEW DATA TYPE: ", data)


if __name__ == "__main__":
    conn = mqtt.Client(client_id="pub", clean_session="True", protocol=mqtt.MQTTv31, transport="tcp")

    conn.on_message = on_message

    conn.connect("localhost")
    conn.subscribe("traffic/pub")

    conn.loop_start()

    pw = input("What is the password? ")

    conn.publish(lights_topic, pw)

    while True:
        if not auth_status:
            print("WAITING FOR AUTH...")

        elif not waiting:
            command = input("What is your command (H for help)?").upper()

            if command == 'H':
                print("Traffic Lights Controller Program")
                print("----")
                print("H - shows this help message")
                print("L - gets current light direction")
                print("N, S, E, W - sends car to lights")
                print("US, UK - set country")

            # send request for light status and wait
            elif command == 'L':
                conn.publish(lights_topic, command)

                waiting = True

            # commands available for forwarding
            elif command in ['N', 'S', 'E', 'W', 'US', 'UK']:
                conn.publish(lights_topic, command)

            # quit the program
            elif command == 'Q':
                break

            else:
                print("INVALID COMMAND")

        time.sleep(1)

    conn.loop_stop()
