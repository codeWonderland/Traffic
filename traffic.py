import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time


class TrafficLights:
    # Grab important pins
    ns_red = 18
    ns_yellow = 23
    ns_green = 24
    ew_red = 25
    ew_yellow = 8
    ew_green = 7

    def __init__(self):
        # Set GPIO to BCM
        GPIO.setmode(GPIO.BCM)

        # create client
        self.client = None

        # direction bool
        self.ns = True

        # set up timers
        self.timer_one = False
        self.timer_two = 0

        # allow waiting for light
        self.ns_waiting = 0
        self.ew_waiting = 0

        # Setup pins for output
        GPIO.setup(TrafficLights.ns_red, GPIO.OUT)
        GPIO.setup(TrafficLights.ns_yellow, GPIO.OUT)
        GPIO.setup(TrafficLights.ns_green, GPIO.OUT)
        GPIO.setup(TrafficLights.ew_red, GPIO.OUT)
        GPIO.setup(TrafficLights.ew_yellow, GPIO.OUT)
        GPIO.setup(TrafficLights.ew_green, GPIO.OUT)

        # Setup start positions
        GPIO.output(TrafficLights.ns_green, True)
        GPIO.output(TrafficLights.ew_red, True)
        GPIO.output(TrafficLights.ns_yellow, False)
        GPIO.output(TrafficLights.ns_red, False)
        GPIO.output(TrafficLights.ew_yellow, False)
        GPIO.output(TrafficLights.ew_green, False)

    def swap_n2w(self):
        if self.ns:
            GPIO.output(TrafficLights.ns_green, False)
            GPIO.output(TrafficLights.ns_yellow, True)
            time.sleep(1)
            GPIO.output(TrafficLights.ns_yellow, False)
            GPIO.output(TrafficLights.ns_red, True)
            GPIO.output(TrafficLights.ew_red, False)
            GPIO.output(TrafficLights.ew_green, True)

    def swap_w2n(self):
        if not self.ns:
            GPIO.output(TrafficLights.ew_green, False)
            GPIO.output(TrafficLights.ew_yellow, True)
            time.sleep(1)
            GPIO.output(TrafficLights.ew_yellow, False)
            GPIO.output(TrafficLights.ew_red, True)
            GPIO.output(TrafficLights.ns_red, False)
            GPIO.output(TrafficLights.ns_green, True)

    def on_message(self, client, userdata, message):
        data = str(message.payload.decode("utf-8")).upper()

        if data in ['N', 'S']:
            self.ns_waiting += 1

        elif data in ['E', 'W']:
            self.ew_waiting += 1

        elif data == 'L':
            dir = 'N'

            if not self.ns:
                dir = 'W'

            self.client.publish("traffic/pub", dir)

        self.timer_one = True

    def run(self):
        # Create client
        self.client = mqtt.Client(client_id="traffic_control",
                             clean_session=True,
                             transport="tcp",
                             protocol=mqtt.MQTTv31)

        # Set Message Callback
        self.client.on_message = self.on_message

        # Connect to broker
        self.client.connect("localhost")
        self.client.subscribe("traffic/lights")

        self.client.loop_start()

        while True:
            self.timer_two = 0

            if self.ew_waiting == 0:
                if not self.ns:
                    self.swap_w2n()

                if self.ns_waiting > 0:
                    self.ns_waiting -= 1

            else:
                self.swap_n2w()

                if self.ew_waiting > 0:
                    self.ew_waiting -= 1
                time.sleep(2.0)
                self.timer_two = 0

                if self.timer_one:
                    self.timer_one = False

                    while self.timer_two != 3:
                        time.sleep(1)
                        self.timer_two += 1

                        if self.ew_waiting > 0:
                            self.ew_waiting -= 1

                self.swap_w2n()

            time.sleep(0)

    def __del__(self):
        # Cleanup GPIO
        GPIO.cleanup()


if __name__ == "__main__":
    lights = TrafficLights()

    try:
        lights.run()

    finally:
        print("Loop Ended")
