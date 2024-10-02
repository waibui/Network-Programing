import socket
import threading
import time
import signal
import sys

class ServerTime:
    def __init__(self, host='127.0.0.1', port=5555):
        self.__host = host
        self.__port = port
        self.total_client = 0
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.__host, self.__port))
        self.server_socket.listen(5)
        
    def run(self):
        print(f'[Server started]: {self.__host}:{self.__port}')
        while True:
            try:
                client_socket, address = self.server_socket.accept()
                pause_event = threading.Event()
                pause_event.set()
                threading.Thread(target=self.handle_client, args=(client_socket, address, pause_event)).start()
                threading.Thread(target=self.send_time, args=(client_socket, pause_event)).start()
            except Exception as e:
                print(f'[Error]: {e}')
                
    def handle_client(self, client_socket, address, pause_event):
        print(f'[Connected]: {address[0]}:{address[1]}')
        self.total_client += 1
        while True:
            try:
                data = client_socket.recv(1024)
                message = data.decode('utf-8')
                if message == "logout":
                    print(f'[Disconnected]: {address[0]}:{address[1]}')
                    self.total_client -= 1
                    break
                elif message == "pause":
                    print(f'[Paused]: {address[0]}:{address[1]}')
                    pause_event.clear()
                elif message == "resume":
                    print(f'[Resumed]: {address[0]}:{address[1]}')
                    pause_event.set()
                    
            except Exception as e:
                print(f'[Error]: {e}')
                break
        client_socket.close()

    def send_time(self, client_socket, pause_event):
        while True:
            pause_event.wait()
            try:
                if client_socket.fileno() == -1:
                    break
                current_time = time.strftime("%H:%M:%S").encode()
                client_socket.send(current_time)
            except Exception as e:
                print(f'[Error]: {e}')
                break
            time.sleep(1)

    @property
    def host(self):
        return self.__host

    @host.setter
    def host(self, value):
        self.__host = value

    @property
    def port(self):
        return self.__port

    @port.setter
    def port(self, value):
        self.__port = value

if __name__ == '__main__':
    server = ServerTime()
    server.run()
