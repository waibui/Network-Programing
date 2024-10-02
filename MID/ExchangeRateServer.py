import socket
import time
import random
import threading

server_address = ('localhost', 49200)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(server_address)
print("[-] SERVER STARTED")

current_data = {}

def get_change_rate():
    rates = {
        'Tokyo': round(random.uniform(1, 1000), 2),
        'Paris': round(random.uniform(1000, 2000), 2),
        'Seoul': round(random.uniform(2000, 3000), 2)
    }
    current_time = time.strftime("%H:%M:%S", time.localtime())
    return {
        'time': current_time,
        'rates': rates
    }

def update_data():
    global current_data
    while True:
        current_data = get_change_rate()
        time.sleep(1)

threading.Thread(target=update_data, daemon=True).start()

while True:
    try:
        message, client_address = server_socket.recvfrom(4096)
        data_to_send = str(current_data).encode()
        server_socket.sendto(data_to_send, client_address)       
    except Exception as e:
        print(e)
