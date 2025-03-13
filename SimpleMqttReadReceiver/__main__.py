from dotenv import load_dotenv
import os
import logging
import paho.mqtt.client as mqtt

load_dotenv()

class MQTTSenderReceiver:
    def __init__(self):
        # Configure logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.client = mqtt.Client(protocol=mqtt.MQTTv5, callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
        self._setup_callbacks()

    def _setup_callbacks(self):
        # Set up callbacks
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_publish = self.on_publish

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
                self.client.username_pw_set(os.getenv('MQTT_USERNAME'), os.getenv('MQTT_PASSWORD'))
            self.client.connect(os.getenv('MQTT_HOST'), int(os.getenv('MQTT_PORT')))
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
    mqtt_sender_receiver.connect(with_account=True)
    mqtt_sender_receiver.subscribe()
    mqtt_sender_receiver.publish(f'{os.getenv("MQTT_USERNAME")}/Boogie', 'Hello World!')
    mqtt_sender_receiver.start_loop()