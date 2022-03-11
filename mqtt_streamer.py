# Importing Libraries
import cv2 as cv
import numpy as np
import paho.mqtt.client as mqtt
import base64
import time
from multiprocessing import Process

# Raspberry PI IP address
MQTT_BROKER = "140.113.179.82"


def post_streamer():
    encoding_parameters = [int(cv.IMWRITE_JPEG_QUALITY), 10]
    # Topic on which frame will be published
    MQTT_SEND = "video/streamer"
    # Object to capture the frames
    cap = cv.VideoCapture(0)
    cap.set(3, 320)
    cap.set(4, 240)
    # Phao-MQTT Clinet
    client = mqtt.Client()
    # Establishing Connection with the Broker
    client.connect(MQTT_BROKER, 10127, 60)
    try:
        while True:
            start = time.time()
            # Read Frame
            _, frame = cap.read()
            # Encoding the Frame
            _, buffer = cv.imencode('.jpg', frame, encoding_parameters)
            # Converting into encoded bytes
            jpg_as_text = base64.b64encode(buffer)
            # Publishig the Frame on the Topic home/server
            client.publish(MQTT_SEND, jpg_as_text)
            end = time.time()
            t = end - start
            fps = 1/t
            print(fps)
    except:
        cap.release()
        client.disconnect()
        print("\nNow you can restart fresh")



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
        cv.imshow("Streamer: from gamer", frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    # Stop the Thread
    client.loop_stop()



if __name__ == '__main__':
    p1= Process(target = post_streamer)
    p2= Process(target = get_gamer)
    p1.start()
    p2.start()

    p1.join()
    p2.join()