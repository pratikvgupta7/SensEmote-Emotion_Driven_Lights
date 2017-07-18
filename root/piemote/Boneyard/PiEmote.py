import socket
import time 
import requests
import cv2
import operator
import numpy as np
#from __future__ import print_function

from bitstruct import pack, byteswap, calcsize
from binascii import hexlify
################################################# This is the non modular functioning version 10/23/2016 - PVG

# Capture raw image from picamera
from picamera import PiCamera
from time import sleep


# Import library to display results
#import matplotlib.pyplot as plt
#%matplotlib inline 
# Display images within Jupyter

_url = 'https://api.projectoxford.ai/emotion/v1.0/recognize'
_key = '17cda856f43d4c7f99fa490b149bd63d'
_maxNumRetries = 10



frame_header_format = 'u16u2u1u1u12u32'
frame_header_byteswap = '224'

frame_address_format = 'u64u48u6u1u1u8'
frame_address_byteswap = '8611'

protocol_header_format = 'u64u16u16'
protocol_header_byteswap = '822'

def send_packet(packet):
    # Broadcast the packet as a UDP message to all bulbs on the network. (Your broadcast IP address may vary?)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(packet, ("192.168.0.255", 56700))
    return (sock.getsockname())
def sizeof(format):
    return calcsize(format)

def make_frame_header(size, origin, tagged, addressable, protocol, source):
    # Make the frame header, specifying the size of the whole packet, the origin, whether it's tagged and addressable,
    # what protocol it uses, and what source it comes from)
    unswapped_header = pack(frame_header_format, size, origin, tagged, addressable, protocol, source)
    #print "\nunswapped frame header: %s" % hexlify(unswapped_header)
    frame_header = byteswap(frame_header_byteswap, unswapped_header)
    #print "frame header: %s" % hexlify(frame_header)
    return frame_header

def make_frame_address(target, ack_required, res_required, sequence):
    # Make the frame address header, specifying the target, whether acknowledgement or response are required, and what
    # number packet in the current sequence this is.
    unswapped_header = pack(frame_address_format, target, 0, 0, ack_required, res_required, sequence)
    #print "\nunswapped frame address: %s" % hexlify(unswapped_header)
    frame_address = byteswap(frame_address_byteswap, unswapped_header)
    #print "frame address: %s" % hexlify(frame_address)
    return frame_address

def make_protocol_header(message_type):
    # Make the protocol header, specifying the message type.
    unswapped_header = pack(protocol_header_format, 0, message_type, 0)
    #print "\nunswapped protocol header: %s" % hexlify(unswapped_header)
    protocol_header = byteswap(protocol_header_byteswap, unswapped_header)
    #print "protocol header: %s" % hexlify(protocol_header)
    return protocol_header

def set_color(hue, saturation, brightness, kelvin, duration):
    # Set the colour of the bulb, based on the input values.

    # Set the format of the payload for this type of message
    payload_format = 'u8u16u16u16u16u32'
    payload_byteswap = '122224'

    # Use the payload format and the header formats to calculate the total size of the packet, in bytes
    packet_size = (sizeof(frame_header_format + frame_address_format + protocol_header_format + payload_format)) / 8
    #print "\npacket size is %s" % packet_size

    # CREATE THE HEADERS
    # 1. Frame header: use packet_size to indicate the length, set origin to 0, set tagged to 1 (because we want all bulbs
    # to respond to it), set addressable to 1, set protocol to 1024, set source to 0 (because we're a dumb client and
    # don't care about responses).
    frame_header = make_frame_header(packet_size, 0, 1, 1, 1024, 1)
    # 2. Frame address: set target to 0 (because we want all bulbs to respond), set ack_required and res_required to 0
    # (because we don't need an acknowledgement or response), and sequence number to 0 (because it doesn't matter what
    # order in the sequence this message is).
    frame_address = make_frame_address(0, 1, 0, 0)
    # 3. Protocol header: set message type to 102, which is a "SetColor" message.
    protocol_header = make_protocol_header(102)
    # 4. Add all the headers together.
    header = frame_header + frame_address + protocol_header

    # CREATE THE PAYLOAD
    # 1. Convert the colours into the right format
    hue = int((float(hue) / 360) * 65535)
    saturation = int(float(saturation) * 65535)
    brightness = int(float(brightness) * 65535)
    kelvin = int(kelvin)
    duration = int(duration)
    #print "\nhue %s %s\nsaturation %s %s\nbrightness %s %s\nkelvin %s %s\nduration %s %s" % (hue, hex(hue), saturation, hex(saturation), brightness, hex(brightness), kelvin, hex(kelvin), duration, hex(duration))
    # 2. Pack the payload information
    unswapped_payload = pack (payload_format, 0, hue, saturation, brightness, kelvin, duration)
    #print "\nunswapped payload: %s" % hexlify(unswapped_payload)
    payload = byteswap(payload_byteswap, unswapped_payload)
    #print "payload: %s" % hexlify(payload)

    # CREATE THE PACKET AND SEND IT
    packet = header + payload
    c , addr = send_packet(packet)
    return c, addr



	
def processRequest( json, data, headers, params ):

    """
    Helper function to process the request to Project Oxford

    Parameters:
    json: Used when processing images from its URL. See API Documentation
    data: Used when processing image read from disk. See API Documentation
    headers: Used to pass the key information and the data type request
    """

    retries = 0
    result = None

    while True:

        response = requests.request( 'post', _url, json = json, data = data, headers = headers, params = params )

        if response.status_code == 429: 

            print( "Message: %s" % ( response.json()['error']['message'] ) )

            if retries <= _maxNumRetries: 
                time.sleep(1) 
                retries += 1
                continue
            else: 
                print( 'Error: failed after retrying!' )
                break

        elif response.status_code == 200 or response.status_code == 201:

            if 'content-length' in response.headers and int(response.headers['content-length']) == 0: 
                result = None 
            elif 'content-type' in response.headers and isinstance(response.headers['content-type'], str): 
                if 'application/json' in response.headers['content-type'].lower(): 
                    result = response.json() if response.content else None 
                elif 'image' in response.headers['content-type'].lower(): 
                    result = response.content
        else:
            print( "Error code: %d" % ( response.status_code ) )
            print( "Message: %s" % ( response.json()['error']['message'] ) )

        break
        
    return result

def renderResultOnImage( result, img ):
    
    """Display the obtained results onto the input image"""

    for currFace in result:
        
        currEmotion = max(currFace['scores'].items(), key=operator.itemgetter(1))[0]
        return currEmotion

# Take images from picamera
camera = PiCamera()
camera.hflip = True
camera.vflip = True
#camera.start_preview()
sleep(2)
camera.capture('/piemote/image.jpg')
#preimg = cv2.imread('/piemote/image.jpg',1)
#cv2.imshow('image',preimg)

# Load raw image file into memory
#pathToFileInDisk = r'C:\Users\PratikV\Pictures\Camera Roll\2.jpg'
pathToFileInDisk = r'/piemote/image.jpg'
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
        s.settimeout(0.2)
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
