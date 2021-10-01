info_msg=(
"""
Sets up a MQTT broker on localhost. 
Used to handle MQTT communication for smart controller.
"""
)

import paho.mqtt.client as mqtt



class MQTT_manager:
    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe("CSI/ESP_STA")
        client.subscribe("CSI/ESP_MS")

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))

    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.client.connect("localhost", 1883, 60)

        # Blocking call that processes network traffic, dispatches callbacks and
        # handles reconnecting.
        # Other loop*() functions are available that give a threaded interface and a
        # manual interface.
        self.client.loop_forever()

if __name__ == "__main__":
    mgr = MQTT_manager()