# Importing Libraries
import tkinter as tk
import tkinter.font as font
import base64
import cv2 as cv
import numpy as np
import paho.mqtt.client as mqtt
from multiprocessing import Process
from PIL import Image, ImageTk
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-x", "--axisX", help="Set the frame width", dest="Axis_X", default="320")
#parser.add_argument("-y", "--axisY", help="Set the frame hight", dest="opt", default="240")
args = parser.parse_args()


MQTT_BROKER = "140.113.179.82"
FRAME_X = 512
FRAME_Y = 480
COMPRESS_QUALITY = 10



def get_streamer():
    MQTT_RECEIVE = "video/streamer"
    global frame 
    frame = cv.imread('wait_for_streamer.jpg')
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
        frame = cv.imdecode(npimg, 1)


    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER, 10127, 60)

    # Starting thread which will receive the frames
    client.loop_start()
    while True:
        cv.imshow("Audience: from streamer", frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    # Stop the Thread
    client.loop_stop()

    

def get_gamer():
    MQTT_RECEIVE = "video/gamer"
    gamer_not_ready = True
    global frame 
    frame = cv.imread('wait_for_gamer.jpg')
    frame = cv.resize(frame, (FRAME_X, FRAME_Y), interpolation=cv.INTER_AREA)
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
        cv.imshow("Audience: from gamer", frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
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

def hi():
    print(hi)



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

    img = Image.open('./start.png')
    #img = img.resize( (img.width // 2, img.height // 2) )
    imgTk =  ImageTk.PhotoImage(img)
    label_image = tk.Label(div1, bg='orange', image=imgTk)
    label_image.grid(column=0, row=0, sticky=align_mode)

    myFont1 = font.Font(family='Helvetica', size=30, weight='bold', slant="italic")
    label_text = tk.Label(div2, bg='orange', text='Audience', font=myFont1)
    label_text.grid(column=0, row=0, sticky=align_mode)

    window.mainloop()

    p1= Process(target = get_streamer)
    p2= Process(target = get_gamer)
    p1.start()
    p2.start()

    p1.join()
    p2.join()