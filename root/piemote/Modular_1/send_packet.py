def send_packet(packet):
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	bcastf = open('/piemote/bcastip','r')
	bcast = bcastf.readline().rstrip()
	bcastf.close
        sock.sendto(packet, (str(bcast), 56700))
        return (sock.getsockname())
