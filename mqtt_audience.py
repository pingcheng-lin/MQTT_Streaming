import base64
import cv2 as cv
import numpy as np
import paho.mqtt.client as mqtt
from multiprocessing import Process

MQTT_BROKER = "140.113.179.82"


def get_streamer():
    MQTT_RECEIVE = "video/streamer"
    global frame 
    frame = np.zeros((240, 320, 3), np.uint8)
    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe(MQTT_RECEIVE)


    # The callback for when a PUBLISH message is received from the server.
    def on_message(client, userdata, msg):
        global frame
        # Decoding the message
        img = base64.b64decode(msg.payload)
        # converting into numpy array from buffer
        npimg = np.frombuffer(img, dtype=np.uint8)
        # Decode to Original Frame
        frame = cv.imdecode(npimg, 1)


    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER, 10127, 60)

    # Starting thread which will receive the frames
    client.loop_start()
    while True:
        cv.imshow("Streamer_Stream", frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    # Stop the Thread
    client.loop_stop()

def get_gamer():
    MQTT_RECEIVE = "video/gamer"
    gamer_not_ready = True
    global frame 
    frame = np.zeros((240, 320, 3), np.uint8)
    #frame = Queue()
    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe(MQTT_RECEIVE)


    # The callback for when a PUBLISH message is received from the server.
    def on_message(client, userdata, msg):
        global frame
        # Decoding the message
        img = base64.b64decode(msg.payload)
        # converting into numpy array from buffer
        npimg = np.frombuffer(img, dtype=np.uint8)
        # Decode to Original Frame
        frame = cv.imdecode(npimg, 1)
        


    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER, 10127, 60)

    # Starting thread which will receive the frames
    client.loop_start()
    while True:
        cv.imshow("Gamer_Stream", frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    # Stop the Thread
    client.loop_stop()

if __name__ == '__main__':
    p1= Process(target = get_streamer)
    p2= Process(target = get_gamer)
    p1.start()
    p2.start()

    p1.join()
    p2.join()