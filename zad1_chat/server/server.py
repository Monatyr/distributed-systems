import socket
from threading import Thread
from server.client_object import Client
import sys


class Server:

    def __init__(self):
        self.server_port = 9876
        self.server_address = '127.0.0.1'
        self.buffer_size = 4096
        self.clients = []
        self.tcp_socket = None
        self.udp_socket = None
        self.num_of_users = 0


    def run(self):
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.bind((self.server_address, self.server_port))
        self.tcp_socket.listen()

        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.bind((self.server_address, self.server_port))

        tcp_thread = Thread(target=self.tcp_loop)
        udp_thread = Thread(target=self.udp_loop)
        server_control_thread = Thread(target=self.server_handle)

        tcp_thread.start()
        udp_thread.start()
        server_control_thread.start()



    def tcp_loop(self):
        while True:
            try:
                conn, addr = self.tcp_socket.accept()
                current_client = Client(conn, addr)
                self.clients.append(current_client)
                
                client_thread = Thread(target=self.tcp_client_handle, args=[current_client])
                client_thread.start()
            except Exception as e:
                sys.exit()



    def udp_loop(self):
        while True:
            try:
                message, addr = self.udp_socket.recvfrom(self.buffer_size)
                print(f"Udp message from {addr}")
                for client in self.clients:
                    if client.get_address() != addr:
                        client.send_message_udp(message, self.udp_socket)
            except Exception as e:
                sys.exit()


    
    def tcp_client_handle(self, current_client: Client):
        self.num_of_users += 1
        current_client.set_name(f'User{self.num_of_users}')
        current_client.send_message_tcp(bytes(f'User{self.num_of_users}', 'utf-8'), '')
        print(current_client.get_name() + " logged in")
        while True:
            try:
                curr_socket = current_client.get_tcp_socket()
                data = curr_socket.recv(self.buffer_size)
                if not data:
                    continue

                print(f"Tcp message from {current_client.get_name()}")

                if str(data, 'utf-8')[:2] == '/q' or str(data, 'utf-8')[:2] == '/Q':
                    curr_socket.close()
                    self.clients.remove(current_client)
                    print(f'{current_client.get_name()} logged out')
                    sys.exit()
                
                for client in self.clients:
                    if client is not current_client:
                        Thread(target=client.send_message_tcp, args=[data, current_client.get_name()]).start()
            except Exception as e:
                sys.exit()


    def server_handle(self):
        while True:
            cmd = input()
            if cmd == '/q' or cmd == '/Q':
                for client in self.clients:
                    msg = bytes(cmd, 'utf-8')
                    client.send_message_tcp(msg, 'Server')
                    client.get_tcp_socket().close()
                self.tcp_socket.close()
                self.udp_socket.close()
                sys.exit()