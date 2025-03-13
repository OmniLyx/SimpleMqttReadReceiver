from dotenv import load_dotenv
import os
import logging
import paho.mqtt.client as mqtt

load_dotenv()


class MQTTSenderReceiver:
    def __init__(self):
        # Configure logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.info('MQTT Sender/Receiver initialized')
        self.client = mqtt.Client(protocol=mqtt.MQTTv5, callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
        self._setup_callbacks()

    def _setup_callbacks(self):
        # Set up callbacks
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_publish = self.on_publish
        self.client.on_message = self.on_message
    
    def update_callbacks(self, on_connect=None, on_disconnect=None, on_publish=None, on_message=None):
        if on_connect:
            self.client.on_connect = on_connect
        if on_disconnect:
            self.client.on_disconnect = on_disconnect
        if on_publish:
            self.client.on_publish = on_publish
        if on_message:
            self.client.on_message = on_message
            
    def on_message(self, client, userdata, message):
        logging.info(f"Received message '{str(message.payload.decode())}' on topic '{message.topic}'")
        # Do something with the message
        # For example, send a response
        # self.publish(message.topic, f"Received message '{str(message.payload.decode())}' on topic '{message.topic}'")

    def on_connect(self, client, userdata, flags, rc, properties=None):
        logging.info("Connected to MQTT broker with result code " + str(rc))

    def on_disconnect(self, client, userdata, disconnect_flags, rc, properties=None):
        logging.info(f"Disconnected from MQTT broker with result code {rc}")
        logging.info(f"Disconnect flags: {disconnect_flags}")
        logging.info(f"Properties: {properties}")

    def on_publish(self, client, userdata, mid, rc, properties=None):
        logging.info("Message published with mid " + str(mid))

    def connect(self, with_account=False):
        try:
            
            if with_account:
                logging.info("Connecting to MQTT broker with account: " + os.getenv('MOSQY_USERNAME'))
                self.client.username_pw_set(os.getenv('MOSQY_USERNAME'), os.getenv('MOSQY_PASSWORD'))
            self.client.connect(os.getenv('MOSQY_HOST'), int(os.getenv('MOSQY_PORT')))
            logging.info("Connected to MQTT broker")
        except Exception as e:
            logging.error(f"Failed to connect to MQTT broker: {e}")
            raise

    def subscribe(self, topic="#"):
        try:
            self.client.subscribe(topic, qos=1)
            logging.info(f"Subscribed to topic {topic}")
        except Exception as e:
            logging.error(f"Failed to subscribe to topic: {e}")
            raise

    def publish(self, topic, message, close_connection=False):
        try:
            self.client.publish(topic, message)
            logging.info(f"Sent message '{message}' to topic '{topic}'")
        except Exception as e:
            logging.error(f"Failed to publish message: {e}")
        finally:
            if close_connection:
                self.client.disconnect()
                logging.info("Connection closed")

    def start_loop(self):
        self.client.loop_forever()

if __name__ == "__main__":
    mqtt_sender_receiver = MQTTSenderReceiver()
    mqtt_sender_receiver._setup_callbacks()
    mqtt_sender_receiver.connect(with_account=True)
    mqtt_sender_receiver.subscribe()
    # mqtt_sender_receiver.publish(f'{os.getenv("MOSQY_USERNAME")}/Boogie', 'Hello World!')
    mqtt_sender_receiver.start_loop()