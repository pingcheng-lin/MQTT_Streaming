# Importing Libraries
import tkinter as tk
import tkinter.font as font
import pyautogui
import cv2 as cv
import numpy as np
import paho.mqtt.client as mqtt
import base64
import time
from multiprocessing import Process
from PIL import Image, ImageTk

# Constant
CAMARA_STREAM = int(1)
SCREEN_SHARE_STREAM = int(2)
STREAM_MODE = CAMARA_STREAM

MQTT_BROKER = "140.113.179.82"
FRAME_X = 320
FRAME_Y = 240
COMPRESS_QUALITY = 10



def post_gamer(MODE):
  encoding_parameters = [int(cv.IMWRITE_JPEG_QUALITY), COMPRESS_QUALITY]
  # Topic on which frame will be published
  MQTT_SEND = "video/gamer"
  # Object to capture the frames
  if MODE == CAMARA_STREAM:
    cap = cv.VideoCapture(0)
    cap.set(3, FRAME_X)
    cap.set(4, FRAME_Y)

  # Phao-MQTT Clinet
  client = mqtt.Client()
  # Establishing Connection with the Broker
  client.connect(MQTT_BROKER, 10127, 60)

  try:
    while True:
      #start = time.time()
      # Read Frame
      if MODE == CAMARA_STREAM:
        _, frame = cap.read()
      elif MODE == SCREEN_SHARE_STREAM:
        screen = pyautogui.screenshot()
        frame = np.array(screen)
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        frame = cv.resize(frame, (FRAME_X, FRAME_Y), interpolation=cv.INTER_AREA)
      # Encoding the Frame
      _, buffer = cv.imencode('.jpg', frame, encoding_parameters)
      # Converting into encoded bytes
      jpg_as_text = base64.b64encode(buffer)
      # Publishig the Frame on the Topic home/server
      client.publish(MQTT_SEND, jpg_as_text)
      #end = time.time()
      #t = end - start
      #fps = 1/t
      #print(fps)
  except:
    cap.release()
    client.disconnect()
    print("\nNow you can restart fresh")



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

def Set_to_camara_mode():
    global STREAM_MODE
    STREAM_MODE = CAMARA_STREAM

def Set_to_screen_share_mode():
    global STREAM_MODE
    STREAM_MODE = SCREEN_SHARE_STREAM



if __name__ == '__main__':
    window = tk.Tk()
    window.title("比賽場地")
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
    div3.grid(column=0, row=2, padx=pad, pady=pad)
    define_layout(window, cols=1, rows=3)
    define_layout([div1, div2, div3])

    img = Image.open('./start.png')
    #img = img.resize( (img.width // 2, img.height // 2) )
    imgTk =  ImageTk.PhotoImage(img)
    label_image = tk.Label(div1, bg='orange', image=imgTk)
    label_image.grid(column=0, row=0, sticky=align_mode)

    myFont1 = font.Font(family='Helvetica', size=20, weight='bold', slant="italic")
    label_text = tk.Button(div2, text="Gamer Ready", font=myFont1, bg='#ff0101', fg='#ffffff', width=30, command=window.destroy)
    label_text.grid(column=0, row=0, sticky=align_mode)

    myFont2 = font.Font(family='Helvetica', size=15, weight='bold')
    btn_camera = tk.Button(div3, text="Set to Camera Stream", font=myFont2, bg='#0052cc', fg='#ffffff', width=22, command=Set_to_camara_mode)
    btn_screen = tk.Button(div3, text="Set to Screen Sharing", font=myFont2, bg='#0052cc', fg='#ffffff', width=22, command=Set_to_screen_share_mode)
    btn_camera.grid(column=0, row=0)
    btn_screen.grid(column=1, row=0)

    window.mainloop()

    #Start Streaming
    p1= Process(target = post_gamer(STREAM_MODE))
    p1.start()

    p1.join()