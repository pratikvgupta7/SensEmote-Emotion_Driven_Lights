import socket
import time
import cv2
import numpy as np
from binascii import hexlify
from picamera import PiCamera
from time import sleep
from processRequest import *
from renderResultOnImage import *
from set_color import *

#	Microsoft Cognitive Service Subscription key 
_key = '17cda856f43d4c7f99fa490b149bd63d'
#	Socket timeout value in seconds
_timeout = 0.2
#	File path to save the camera image
#pathToFileInDisk = r'C:\Users\PratikV\Pictures\Camera Roll\2.jpg'
pathToFileInDisk = r'/piemote/image.jpg'
#	Wait time between initializing and operating camera in seconds
_camerawait = 2

# Take images from picamera
camera = PiCamera()
camera.hflip = True
camera.vflip = True
sleep(_camerawait)
camera.capture(pathToFileInDisk)

# Load raw image file into memory

with open( pathToFileInDisk, 'rb' ) as f:
    data = f.read()
headers = dict()
headers['Ocp-Apim-Subscription-Key'] = _key
headers['Content-Type'] = 'application/octet-stream'
json = None
params = None
result = processRequest( json, data, headers, params )

if result is not None:
    # Load the original image from disk
    data8uint = np.fromstring( data, np.uint8 ) # Convert string to an unsigned int array
    img = cv2.cvtColor( cv2.imdecode( data8uint, cv2.IMREAD_COLOR ), cv2.COLOR_BGR2RGB )
    emores = renderResultOnImage( result, img )
    emotion = str(emores)

if emotion == 'happiness':
    hue = 330
    saturation = 1
    brightness = 0.4
    kelvin = 2500
    duration = 1000
elif emotion == 'neutral':
    hue = 90
    saturation = 0.1
    brightness = 0.5
    kelvin = 2500
    duration = 1000
print (emotion)
count = 0
while True:
    ip, port = set_color(hue, saturation, brightness, kelvin, duration)
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.settimeout(_timeout)
    s.bind(("", port))
    count += 1
    print (count)
    print (ip)
    print (port)
    try:
        if count == 21:
            break
        else:
            data,addr = s.recvfrom(1024)
            print ("Connection from" +  str(addr))
            print (data)
            if data.find('-')!= -1:
                print("Data from device" + data)
                break
    except socket.timeout:
        s.close()
