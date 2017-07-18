def set_color(hue, saturation, brightness, kelvin, duration):
    from sizeof import *
    from make_frame_header import *
    from make_frame_address import *
    from make_protocol_header import *
    from send_packet import *
    from bitstruct import pack, byteswap, calcsize
	
	# Set the colour of the bulb, based on the input values.

	# Set the format of the payload for this type of message
    payload_format = 'u8u16u16u16u16u32'
    payload_byteswap = '122224'
    frame_header_format = 'u16u2u1u1u12u32'
    frame_address_format = 'u64u48u6u1u1u8'
    protocol_header_format = 'u64u16u16'

	# Use the payload format and the header formats to calculate the total size of the packet, in bytes
    packet_size = (sizeof(frame_header_format + frame_address_format + protocol_header_format + payload_format)) / 8
    
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
 
	# 2. Pack the payload information
    unswapped_payload = pack (payload_format, 0, hue, saturation, brightness, kelvin, duration)
 
    payload = byteswap(payload_byteswap, unswapped_payload)
 

	# CREATE THE PACKET AND SEND IT
    packet = header + payload
    c , addr = send_packet(packet)
    return c, addr
