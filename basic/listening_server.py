import socket
import argparse

def start_server(port, protocol, host='localhost'):
    if protocol == "tcp":
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    elif protocol == "udp":
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    else:
        exit

    server_socket.bind((host,port))

    if protocol == "tcp":
        server_socket.listen(1)
    
    print("Listening for", protocol,"on port", port)

    while True:
        # TCP uses recv while UDP uses recvfrom
        # This is because TCP is a stream protocol and UDP is a message protocol
        # recv is useful for persistent connections on a specific socket
        # recvfrom is useful when data can come from any client, without a connection
        if protocol == "tcp":
            (client_socket, address) = server_socket.accept()
            print("Accepted connection from",address)
            message = client_socket.recv(1024)
            print("TCP Message:", message.decode())
            client_socket.close()
        elif protocol == "udp":
            message, address = server_socket.recvfrom(1024)
            print("UDP Message from",address, message.decode())


#For testing on localhost on port 4444
#echo "hello tcp" | nc 127.0.0.1 4444
#echo "hello udp" | nc -u 127.0.0.1 4444

parser = argparse.ArgumentParser()
parser.add_argument("protocol", type=str, help="The protocol to use. Values accepted: tcp udp")
parser.add_argument("port", type=int, help="The port to listen on")
args = parser.parse_args()
start_server(args.port, args.protocol)
