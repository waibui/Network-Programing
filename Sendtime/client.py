import socket
import threading
import tkinter as tk
import sys

SERVER_ADDRESS = ('localhost', 12345)

class Client:
    def __init__(self):
        self.setup_gui()
        self.setup_network()
        self.setup_receive_thread()

    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("Client")
        self.root.geometry("300x200")
        self.root.configure(bg="black")
        
        self.server_time = "00:00:00"
        self.root.protocol("WM_DELETE_WINDOW", self.close_connection)

        self.label = tk.Label(self.root, text='Client Time', font=('Helvetica', 16, 'bold'), bg='black', fg='white')
        self.label.pack(side=tk.TOP, pady=10)

        self.time_container = tk.Label(self.root, text=self.server_time, font=('Helvetica', 24), bg='black', fg='lime')
        self.time_container.pack(expand=True)

        self.setup_buttons()

    def setup_buttons(self):
        self.pause_button = tk.Button(self.root, text='Pause', command=self.pause_connection, font=('Helvetica', 12, 'bold'), bg='red', fg='white')
        self.pause_button.pack(side=tk.LEFT, padx=10)

        self.resume_button = tk.Button(self.root, text='Resume', command=self.resume_connection, font=('Helvetica', 12, 'bold'), bg='green', fg='white')
        self.resume_button.pack(side=tk.RIGHT, padx=10)

    def setup_network(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_socket.sendto("START".encode('utf-8'), SERVER_ADDRESS)

    def setup_receive_thread(self):
        self.receive_thread = threading.Thread(target=self.receive_time, daemon=True)
        self.receive_thread.start()

    def receive_time(self):
        while True:
            try:
                data, _ = self.client_socket.recvfrom(1024)
                if data:
                    self.server_time = data.decode('utf-8')
                    self.time_container.config(text=self.server_time)
                else:
                    print("No data received.")
            except Exception as e:
                print(f"Error receiving data: {e}")

    def pause_connection(self):
        self.client_socket.sendto("PAUSE".encode(), SERVER_ADDRESS)

    def resume_connection(self):
        self.client_socket.sendto("RESUME".encode(), SERVER_ADDRESS)

    def close_connection(self):
        self.client_socket.sendto('STOP'.encode('utf-8'), SERVER_ADDRESS)
        self.client_socket.close()
        self.root.destroy()
        sys.exit(0)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    client = Client()
    client.run()
