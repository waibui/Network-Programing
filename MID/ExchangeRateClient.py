import socket
import threading
import tkinter as tk
from tkinter import ttk
import sys
import time
import ast

SERVER_ADDRESS = ('localhost', 49200)

class Client:
    def __init__(self):
        self.setup_gui()
        self.setup_network()
        self.pause = False
        self.setup_thread()

    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("Client")
        self.root.geometry("600x400")
        self.root.protocol("WM_DELETE_WINDOW", self.close_connection)

        self.label = tk.Label(self.root, text='Tỷ giá', font=('Helvetica', 16, 'bold'), fg='black')
        self.label.pack(side=tk.TOP, pady=10)

        self.setup_table()
        self.setup_buttons()

    def setup_table(self):
        columns = ("Time", "Tokyo", "Paris", "Seoul")

        self.frame = tk.Frame(self.root)
        self.frame.pack(expand=True, fill=tk.BOTH)

        self.scrollbar = ttk.Scrollbar(self.frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree = ttk.Treeview(self.frame, columns=columns, show="headings", height=5, yscrollcommand=self.scrollbar.set)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor='center')

        self.tree.pack(expand=True, fill=tk.BOTH)

        self.scrollbar.config(command=self.tree.yview)


    def setup_buttons(self):
        self.pause_button = tk.Button(self.root, text='Pause', command=self.pause_connection, font=('Helvetica', 12, 'bold'))
        self.pause_button.pack(side=tk.RIGHT, padx=10, pady=10)

        self.resume_button = tk.Button(self.root, text='Resume', command=self.resume_connection, font=('Helvetica', 12, 'bold'))
        self.resume_button.pack(side=tk.RIGHT, padx=10, pady=10)

    def setup_network(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_socket.sendto("START".encode('utf-8'), SERVER_ADDRESS)

    def setup_thread(self):
        self.send_thread = threading.Thread(target=self.send_request, daemon=True).start()
        self.receive_thread = threading.Thread(target=self.receive_data, daemon=True).start()

    def send_request(self):
        time.sleep(1)
        while True:
            if not self.pause:
                try:
                    self.client_socket.sendto("REQUEST_DATA".encode('utf-8'), SERVER_ADDRESS)
                    time.sleep(1)
                except Exception as e:
                    print(f"Error sending request: {e}")

    def receive_data(self):
        while True:
            if not self.pause:
                try:
                    data, _ = self.client_socket.recvfrom(1024)
                    if data:
                        data_str = data.decode('utf-8')
                        data_dict = ast.literal_eval(data_str)
                        self.update_table(data_dict)
                    else:
                        print("No data received.")
                except Exception as e:
                    print(f"Error receiving data: {e}")

    def update_table(self, data):
        time_received = data['time']
        rates = data['rates']
        self.tree.insert('', tk.END, values=(time_received, rates['Tokyo'], rates['Paris'], rates['Seoul']))
        self.tree.yview_moveto(1)

    def pause_connection(self):
        self.pause = True
        print(f"[-] PAUSED")
        
    def resume_connection(self):
        self.pause = False
        print(f"[+] RESUMED")
        
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
