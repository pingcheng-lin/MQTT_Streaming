# Importing Libraries
import tkinter as tk
import tkinter.font as font
import base64
import cv2 as cv
import numpy as np
import paho.mqtt.client as mqtt
import argparse
from multiprocessing import Process
from PIL import Image, ImageTk
from ping3 import ping
import matplotlib.pyplot as plt
import logging
import pyaudio

parser = argparse.ArgumentParser()
parser.add_argument("-x", "--axisX", help="Set the frame width", type=int, dest="Axis_X", default=800)
parser.add_argument("-y", "--axisY", help="Set the frame hight", type=int,dest="Axis_Y", default=600)
parser.add_argument("-p", "--ping", help="Set to ping test mode", type=bool,dest="Ping_test", default=False)
args = parser.parse_args()


MQTT_BROKER = "140.113.179.82"
FRAME_X = int(args.Axis_X)
FRAME_Y = int(args.Axis_Y)
PING_TEST_MODE = bool(args.Ping_test)

FORMAT = '%(asctime)s %(levelname)s: %(message)s'
logging.basicConfig(level=logging.DEBUG, filename='log/audience.log', filemode='w', format=FORMAT)



def get_streamer():
    MQTT_RECEIVE = "video/streamer"
    global frame 
    frame = cv.imread('image/wait_for_streamer.jpg')
    frame = cv.resize(frame, (FRAME_X, FRAME_Y), interpolation=cv.INTER_AREA)
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
        frame = cv.resize(cv.imdecode(npimg, 1), (FRAME_X, FRAME_Y), interpolation=cv.INTER_AREA)
        logging.info("get message")


    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER, 10127, 60)

    # Starting thread which will receive the frames
    client.loop_start()
    while True:
        cv.imshow("Audience: from streamer  <Press Q to exit>", frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    # Stop the Thread
    client.loop_stop()

def get_streamer_audio():
    MQTT_RECEIVE = "audio/streamer"
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe(MQTT_RECEIVE)

    global chunks
    chunks = []
    # The callback for when a PUBLISH message is received from the server.
    def on_message(client, userdata, msg):
        global chunks
        # Decoding the message
        data = base64.b64decode(msg.payload)
        chunks.append(data)

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER, 10127, 60)

    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, output=True, frames_per_buffer=1024)
    # Starting thread which will receive the frames
    client.loop_start()
    try:
        while True:
            if len(chunks) > 0:
                stream.write(chunks.pop(0), 1024)
    except KeyboardInterrupt:
        stream.stop_stream()
        stream.close()
        audio.terminate()
    # Stop the Thread
    client.loop_stop()

def get_gamer():
    MQTT_RECEIVE = "video/gamer"
    global frame 
    frame = cv.imread('image/wait_for_gamer.jpg')
    frame = cv.resize(frame, (FRAME_X, FRAME_Y), interpolation=cv.INTER_AREA)
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
        frame = cv.resize(cv.imdecode(npimg, 1), (FRAME_X, FRAME_Y), interpolation=cv.INTER_AREA)
        


    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER, 10127, 60)

    # Starting thread which will receive the frames
    client.loop_start()
    while True:
        cv.imshow("Audience: from gamer  <Press Q to exit>", frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    # Stop the Thread
    client.loop_stop()

def get_gamer_audio():
    MQTT_RECEIVE = "audio/gamer"
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe(MQTT_RECEIVE)

    global chunks
    chunks = []
    # The callback for when a PUBLISH message is received from the server.
    def on_message(client, userdata, msg):
        global chunks
        # Decoding the message
        data = base64.b64decode(msg.payload)
        chunks.append(data)

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER, 10127, 60)

    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, output=True, frames_per_buffer=1024)
    # Starting thread which will receive the frames
    client.loop_start()
    try: 
        while True:
            if len(chunks) > 0:
                stream.write(chunks.pop(0), 1024)
    except KeyboardInterrupt:
        stream.stop_stream()
        stream.close()
        audio.terminate()
    # Stop the Thread
    client.loop_stop()


def define_layout(obj, cols=1, rows=1):
    
    def method(trg, col, row):
        
        for c in range(cols):    
            trg.columnconfigure(c, weight=1)
        for r in range(rows):
            trg.rowconfigure(r, weight=1)

    if type(obj)==list:        
        [ method(trg, cols, rows) for trg in obj ]
    else:
        trg = obj
        method(trg, cols, rows)

def ping_test():
    if PING_TEST_MODE == True:
        delay = []
        for i in range(1, 100):
            delay.append(ping(MQTT_BROKER, unit='ms'))

        plt.plot(delay)
        plt.show()
        


if __name__ == '__main__':
    window = tk.Tk()
    window.title("觀眾場地")
    window.configure(bg='orange')
    align_mode = 'nswe'
    pad = 5

    div1 = tk.Frame(window,  width=1200 , height=200)
    div2 = tk.Frame(window,  width=1200 , height=200)
    div3 = tk.Frame(window,  width=1200 , height=200)

    window.update()
    win_size = min( window.winfo_width(), window.winfo_height())

    div1.grid(column=0, row=0, padx=pad, pady=pad)
    div2.grid(column=0, row=1, padx=pad, pady=pad)
    define_layout(window, cols=1, rows=2)
    define_layout([div1, div2])

    img = Image.open('image/start.png')
    #img = img.resize( (img.width // 2, img.height // 2) )
    imgTk =  ImageTk.PhotoImage(img)
    label_image = tk.Label(div1, bg='orange', image=imgTk)
    label_image.grid(column=0, row=0, sticky=align_mode)

    myFont1 = font.Font(family='Helvetica', size=20, weight='bold', slant="italic")
    label_text = tk.Button(div2, text="Audience Ready", font=myFont1, bg='#ff0101', fg='#ffffff', width=30, command=window.destroy)
    label_text.grid(column=0, row=0, sticky=align_mode)

    window.mainloop()

    p1 = Process(target = get_streamer)
    p1_audio = Process(target = get_streamer_audio)
    p2 = Process(target = get_gamer)
    p2_audio = Process(target = get_gamer_audio)
    p3 = Process(target = ping_test)
    p1.start()
    p1_audio.start()
    p2.start()
    p2_audio.start()
    p3.start()

    p1.join()
    p1_audio.join()
    p2.join()
    p2_audio.join()
    p3.join()