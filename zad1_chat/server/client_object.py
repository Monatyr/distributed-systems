from socket import socket
import sys

class Client:

    def __init__(self, client_socket: socket, address):
        self.tcp_socket = client_socket
        self.address = address
        self.name = None

    
    def send_message_tcp(self, byte_message, name):
        try:
            byte_message = bytes(name + ': ', 'utf-8') + byte_message
            self.tcp_socket.send(byte_message)
        except:
            sys.exit()


    def send_message_udp(self, byte_message, udp_socket):
        try:
            udp_socket.sendto(byte_message, self.address)
        except:
            sys.exit()


    def set_name(self, name):
        self.name = name


    def get_name(self):
        return self.name


    def get_tcp_socket(self) -> socket:
        return self.tcp_socket


    def get_address(self):
        return self.address
