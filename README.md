# MQTT Sender Receiver Library

This is a simple MQTT sender and receiver library implemented in Python using the `paho-mqtt` library. It allows you to connect to an MQTT broker, subscribe to topics, and publish messages.

## Prerequisites

- Python 3.x
- `paho-mqtt` library
- `python-dotenv` library

You can install the required libraries using pip:

```sh
pip install paho-mqtt python-dotenv
```

## Environment Variables

Create a `.env` file in the root directory of your project and add the following environment variables:

```
MQTT_HOST=<your_mqtt_broker_host>
MQTT_PORT=<your_mqtt_broker_port>
MQTT_USERNAME=<your_mqtt_username>
MQTT_PASSWORD=<your_mqtt_password>
```

## Usage

1. **Initialize the MQTTSenderReceiver class:**

    ```python
    from simplemqttreadreceiver import MQTTSenderReceiver

    mqtt_sender_receiver = MQTTSenderReceiver()
    ```

2. **Connect to the MQTT broker:**

    ```python
    mqtt_sender_receiver.connect(with_account=True)
    ```

3. **Subscribe to a topic:**

    ```python
    mqtt_sender_receiver.subscribe(topic="your/topic")
    ```

4. **Publish a message to a topic:**

    ```python
    mqtt_sender_receiver.publish(topic="your/topic", message="Hello World!")
    ```

5. **Start the MQTT client loop:**

    ```python
    mqtt_sender_receiver.start_loop()
    ```

## Example

Here is an example of how to use the library:

```python
from SimpleMQTTSenderReceiver import SimpleMQTTSenderReceiver
import os

if __name__ == "__main__":
    mqtt_sender_receiver = MQTTSenderReceiver()
    mqtt_sender_receiver.connect(with_account=True)
    mqtt_sender_receiver.subscribe(topic=f'{os.getenv("MQTT_USERNAME")}/Boogie')
    mqtt_sender_receiver.publish(topic=f'{os.getenv("MQTT_USERNAME")}/Boogie', message='Hello World!')
    mqtt_sender_receiver.start_loop()
```

## Logging

The library uses Python's built-in logging module to log information about the connection, subscription, and publishing processes. Logs are printed to the console with timestamps and log levels.

## License

Do whatever you want with this code. I am not responsible for any damages caused by the use of this code. Use at your own risk.
```