import paho.mqtt.client as mqtt_client
import random
import configparser
import time
import requests

config = configparser.ConfigParser()
config.read('config.ini')

class MqttClient:
    def __init__(self, address, port):
        self.broker=address
        self.port=port
        self.topics = ['custom-devices/downstream/242895']
        self.data = {
        "command": "setChannelsState",
        "version": 1,
        "data": {
            "hosts": [{
                "address": "192.168.88.15",
                "port": 3192,
                "universes": [{
                    "universe": 17,
                    "channels": [[10, 0, 0], [15, 0, 2]]
                }
                ]
            }
            ]
        }
    }

    def createClient(self):
        # client_id = f'python-mqtt-{random.randint(0, 1000)}'
        client = mqtt_client.Client("P1")
        return client

    def toConnect(self, client):
        client.connect(self.broker, self.port)
        print("I've connected: {}".format(self.broker))


    def toSubscribe(self, client):
        for topic in self.topics:
            client.subscribe(topic)
        print("I've subscribed with QoS: {}".format([topic for topic in self.topics]))

    def on_message(self, client, userdata, message):

        print("message received ", str(message.payload.decode("utf-8")))
        print("message topic=", message.topic)
        print("message qos=", message.qos)
        print("message retain flag=", message.retain)

    def publishData(self, client):
        for topic in self.topics:
            client.publish(topic, str(self.data))

    def setTopic(self, topic):
       self.topics.append(topic)


    def start(self):
        response = requests.get('https://google.com')
        print(response)
        client = self.createClient()
        client.on_message = self.on_message
        self.toConnect(client)
        client.loop_start()
        self.toSubscribe(client)
        self.publishData(client)



if __name__ == '__main__':

    # data = {
    #     "command": "setChannelsState",
    #     "version": 1,
    #     "data": {
    #         "hosts": [{
    #             "address": "192.168.88.15",
    #             "port": 3192,
    #             "universes": [{
    #                 "universe": 17,
    #                 "channels": [[10, 0, 0], [15, 0, 2]]
    #             }
    #             ]
    #         }
    #         ]
    #     }
    # }

    address = config.get('mqtt', 'broker_address')
    port = config.get('mqtt', 'port')
    print(address, port)
    mqttClient = MqttClient(address, int(port))
    mqttClient.start()