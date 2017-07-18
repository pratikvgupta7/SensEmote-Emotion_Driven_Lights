import socket

UDP_IP = "192.168.0.255"
UDP_PORT = 56700

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024)
    print "received message:", data
    print "from address:", str(addr)
