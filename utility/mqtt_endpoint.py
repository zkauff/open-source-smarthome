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
        client.subscribe("iot/admin/acks")

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))

    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.connect()
    
    def connect(self):
        self.client.connect("localhost", 1883, 60)

    def send_command(self, device, message):
        self.connect()
        self.client.publish(device, message)

if __name__ == "__main__":
    """
    Used for quick verification that mosquitto's set up correctly.
    To test, set up a mqtt client that's subscribed to 'iot/dummy/cmd' 
    and see that the message gets to the client. 
    ex:
        mosquitto_sub -d -t iot/dummy/cmd
    """
    MQTT_manager().send_command("dummy", "{ 'message': 'testing broker' }")
