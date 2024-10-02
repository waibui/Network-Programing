import socket

def udp_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.sendto(b"Hello, server!", ("localhost", 12345))
    while True:
        message, server = client_socket.recvfrom(4096)
        print(message.decode())

if __name__ == "__main__":
    udp_client()
