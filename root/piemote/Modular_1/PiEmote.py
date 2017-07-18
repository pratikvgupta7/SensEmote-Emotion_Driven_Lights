import socket
import time
import cv2
import numpy as np
import sqlite3
import RPi.GPIO as GPIO
from binascii import hexlify
from picamera import PiCamera
from time import sleep
from processRequest import *
from renderResultOnImage import *
from set_color import *

GPIO.setmode(GPIO.BCM)
CAMLED = 32
GPIO.setup(CAMLED, GPIO.OUT, initial=False)
#       Microsoft Cognitive Service Subscription key
#_key = ''
with open('/piemote/mskey','r') as keyread:
	_key=keyread.read().replace('\n', '')
#       Socket timeout value in seconds
_timeout = 0.2
#       File path to save the camera image
#pathToFileInDisk = r'C:\Users\PratikV\Pictures\Camera Roll\2.jpg'
pathToFileInDisk = r'/piemote/image.jpg'
#       Wait time between initializing and operating camera in seconds
_camerawait = 2

# Take images from picamera
camera = PiCamera()
camera.hflip = True
camera.vflip = True
GPIO.output(CAMLED,True)
sleep(_camerawait)
camera.capture(pathToFileInDisk)
GPIO.output(CAMLED,False)
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
	emores, emoscore = renderResultOnImage( result, img )
	emotion = str(emores)
	conn=sqlite3.connect('/piemote/neodb/neo.db')
	curs=conn.cursor()
	curs.execute("select hue, sat , bri, kel from emosmith where emo = \"{myemo}\" and low <={mysco} and high >={mysco}".format(myemo = emotion, mysco = emoscore))
	all = curs.fetchall()
	hue = all[0][0]
	saturation = all[0][1]
	brightness = all[0][2]
	kelvin = all[0][3]
	duration = 1000
	print (emotion)
	count = 0
	while True:
		ip, port = set_color(hue, saturation, brightness, kelvin, duration)
		s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		s.settimeout(_timeout)
		s.bind(("", port))
		count += 1
		#print (count)
		#print (ip)
		#print (port)
		try:
			if count == 21:
				break
			else:
				data,addr = s.recvfrom(1024)
				#print ("Connection from" +  str(addr))
				#print (data)
				if data.find('-')!= -1:
					#print("Data from device" + data)
					break
		except socket.timeout:
			s.close()
else:
	pass	
