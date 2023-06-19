from paho.mqtt import client as mqtt_client

class Mqtt:
    def __init__(self,broker,port,client_id):
        self.broker=broker
        self.port=port
        #self.topic=topic
        self.client_id=client_id
        self.client=self.connect()
        self.client.loop_start()

    def connect(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

        client = mqtt_client.Client(self.client_id)
        client.on_connect = on_connect
        client.connect(self.broker, self.port)
        return client

    def publish(self,topic,msg):

        result = self.client.publish(topic, msg)

        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
