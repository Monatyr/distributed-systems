import socket
from threading import Thread
import sys
import struct



class Client:

    def __init__(self):
        self.name = None
        self.server_port = 9876
        self.server_address = '127.0.0.1'
        self.buffer_size = 4096
        self.multicast_group = '224.1.1.1'
        self.multicast_port = 8765
        self.tcp_socket = None
        self.udp_socket = None
        self.udp_multicast_socket = None


    def run(self):
        self.connect_with_server()
        Thread(target=self.write_loop).start()
        Thread(target=self.read_loop).start()


    def connect_with_server(self):
        try:
            self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.tcp_socket.connect((self.server_address, self.server_port))

            self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.udp_socket.bind(('', self.tcp_socket.getsockname()[1]))

            self.udp_multicast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            self.udp_multicast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.udp_multicast_socket.bind(('', self.multicast_port))
            mreq = struct.pack("4sl", socket.inet_aton(self.multicast_group), socket.INADDR_ANY)
            self.udp_multicast_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
            
        except Exception as e:
            print("Error while trying to log in")
            sys.exit()


    def read_loop(self):
        Thread(target=self.tcp_read_loop, daemon=False).start()
        Thread(target=self.udp_read_loop, daemon=False).start()
        Thread(target=self.multicast_udp_read_loop, daemon=False).start()


    def tcp_read_loop(self):
        while True:
            try:
                data = self.tcp_socket.recv(self.buffer_size)
                msg = str(data, 'utf-8')
                if msg[:10] == 'Server: /q' or msg[:2] == 'Server: /Q': #server shutdown
                    self.close_all_sockets()
                    print("Server shut down")
                    sys.exit()
                elif msg[0] == ':': #username
                    self.name = msg[2:]
                else:               #normal message
                    print(str(data, 'utf-8'))
            except Exception as e:
                sys.exit()


    def udp_read_loop(self):
        while True:
            try:
                data, _ = self.udp_socket.recvfrom(self.buffer_size)
                print(str(data, 'utf-8'))
            except Exception as e:
                sys.exit()


    def multicast_udp_read_loop(self):
        while True:
            try:
                data, _ = self.udp_multicast_socket.recvfrom(self.buffer_size)
                if not self.name in str(data, 'utf-8'):
                    print(str(data, 'utf-8'))
            except Exception as e:
                sys.exit()


    def write_loop(self):
        while True:
            try:
                msg = input()
                if msg[:2] == '/u' or msg[:2] == '/U':
                    self.send_ascii_art(msg, self.udp_socket, self.server_address, self.server_port)
                elif msg[:2] == '/m' or msg[:2] == '/M':
                    byte_msg = bytes(msg[2:], 'utf-8')
                    self.send_ascii_art(msg, self.udp_multicast_socket, self.multicast_group, self.multicast_port)
                elif msg[:2] == '/q' or msg[:2] == '/Q':
                    byte_msg = bytes(msg, 'utf-8')
                    self.tcp_socket.send(byte_msg)
                    self.close_all_sockets()
                    sys.exit()
                else:
                    byte_msg = bytes(msg, 'utf-8')
                    self.tcp_socket.send(byte_msg)
            except Exception as e:
                sys.exit()


    def send_ascii_art(self, msg, socket_type: socket.socket, address, port):
        file_name = msg[2:].lstrip()
        try:
            with open(f'ascii_art/{file_name}', 'r') as file:
                msg = f'{self.name}:\n'
                for line in file.readlines():
                    msg += line
                byte_msg = bytes(msg, 'utf-8')
                socket_type.sendto(byte_msg, (address, port))
        except:
            print(f"File '{file_name}' does not exit")


    def close_all_sockets(self):
        self.tcp_socket.close()
        self.udp_socket.close()
        self.udp_multicast_socket.close()



if __name__ == "__main__":
    client = Client()