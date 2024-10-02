import socket
import datetime
import threading
import time

SERVER_ADDRESS = ('localhost', 12345)
TIMEOUT_DURATION = 1

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(SERVER_ADDRESS)
server_socket.settimeout(TIMEOUT_DURATION)

print("[-] Server listening...")

clients = {} 

class ClientHandler(threading.Thread):
    def __init__(self, client_address):
        super().__init__()
        self.client_address = client_address
        self.running = True
        self.paused = False

    def run(self):
        while self.running:
            if not self.paused:
                current_time = datetime.datetime.now().strftime("%H:%M:%S")
                server_socket.sendto(current_time.encode('utf-8'), self.client_address)
            time.sleep(1) 

    def update_state(self, command):
        if command == 'pause':
            self.paused = True
            print(f"[-] {self.client_address} paused")
        elif command == 'resume':
            self.paused = False
            print(f"[-] {self.client_address} resumed")
        elif command == 'stop':
            self.running = False
            print(f"[-] {self.client_address} stopped")

while True:
    try:
        data, client_address = server_socket.recvfrom(1024)
        command = data.decode('utf-8').lower()

        if client_address not in clients:
            client_handler = ClientHandler(client_address)
            clients[client_address] = client_handler
            client_handler.start()
            print(f"[-] {client_address} connected")

        clients[client_address].update_state(command)

    except socket.timeout:
        continue
    except Exception as e:
        print(f"Error: {e}")
