def send_packet(packet):
        import socket
    # Broadcast the packet as a UDP message to all bulbs on the network. (Your broadcast IP address may vary?)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(packet, ("192.168.0.255", 56700))
        return (sock.getsockname())
