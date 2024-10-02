import socket
import time
import threading

def handle_client(client_address):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    while True:
        data, address = client_socket.recvfrom(4096)
        if not data:
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            message = f"Current server time: {current_time}"
            client_socket.sendto(message.encode(), client_address)
            time.sleep(1)

def udp_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 12345)
    server_socket.bind(server_address)
    
    print(f"Server is running on {server_address}")

    while True:
        # Nhận yêu cầu từ client
        message, client_address = server_socket.recvfrom(4096)
        print(f"Connection from {client_address}")

        # Tạo luồng mới để xử lý client
        client_thread = threading.Thread(target=handle_client, args=(client_address,))
        client_thread.start()

if __name__ == "__main__":
    udp_server()
