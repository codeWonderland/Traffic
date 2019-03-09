import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time, threading

# Set GPIO to BCM
GPIO.setmode(GPIO.BCM)

# Grab important pins
ns_red = 18
ns_yellow = 23
ns_green = 24
ew_red = 25
ew_yellow = 8
ew_green = 7

# Setup pins for output
GPIO.setup(ns_red, GPIO.OUT)
GPIO.setup(ns_yellow, GPIO.OUT)
GPIO.setup(ns_green, GPIO.OUT)
GPIO.setup(ew_red, GPIO.OUT)
GPIO.setup(ew_yellow, GPIO.OUT)
GPIO.setup(ew_green, GPIO.OUT)

# Setup start positions
GPIO.output(ns_green, True)
GPIO.output(ew_red, True)
GPIO.output(ns_yellow, False)
GPIO.output(ns_red, False)
GPIO.output(ew_yellow, False)
GPIO.output(ew_green, False)

# direction bool
ns = True

# can swap from ns bool
can_swap = True

# set up timers
timer_one = False
timer_two = 0

# allow waiting for light
ns_waiting = 0
ew_waiting = 0

# Create client
client = mqtt.Client(client_id="traffic_control", clean_session=True, userdata=None, transport="tcp")
protocol = mqtt.MQTTv31


def allow_n2w():
    global can_swap
    can_swap = True

    if ew_waiting > 0:
        swap_n2w()


def swap_n2w():
    if ns and can_swap:
        GPIO.output(ns_green, False)
        GPIO.output(ns_yellow, True)
        time.sleep(1)
        GPIO.output(ns_yellow, False)
        GPIO.output(ns_red, True)
        GPIO.output(ew_red, False)
        GPIO.output(ew_green, True)


def swap_w2n():
    if not ns and can_swap:
        GPIO.output(ew_green, False)
        GPIO.output(ew_yellow, True)
        time.sleep(1)
        GPIO.output(ew_yellow, False)
        GPIO.output(ew_red, True)
        GPIO.output(ns_red, False)
        GPIO.output(ns_green, True)


def on_message(client, userdata, message):
    global ew_waiting
    global ns_waiting
    global timer_one

    data = str(message.payload.decode("utf-8")).upper()

    if data in ['N', 'S']:
        ns_waiting += 1

    elif data in ['E', 'W']:
        ew_waiting += 1

    timer_one = True


# Set Message Callback
client.on_message = on_message

# Connect to broker
client.connect("localhost")
client.subscribe("prof/blinks", qos=0)

try:
    client.loop_forever()

    while True:
        timer_two = 0

        if ew_waiting == 0 and ns_waiting > 0:
            if not ns:
                swap_w2n()

            ns_waiting -= 1

        elif ns_waiting == 0 and ew_waiting > 0:
            swap_n2w()

            ew_waiting -= 1
            time.sleep(2.0)
            timer_two = 0

            if timer_one:
                timer_one = False

                while timer_two != 3:
                    time.sleep(1)
                    timer_two += 1

                    if ew_waiting > 0:
                        ew_waiting -= 1

            swap_w2n()

finally:
    # Cleanup GPIO
    GPIO.cleanup()

