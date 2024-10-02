import socket
import struct
import threading
import tkinter as tk
import json
from tkinter import messagebox, simpledialog

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007

BROADCAST_ADDR = '255.255.255.255'
NORMAL_PORT = 5008

class Multicast:
    def __init__(self):
        self.setup_gui()
        self.sock = self.setup_socket()

    def setup_socket(self):
        """ Set up the UDP socket. """
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        return sock

    def setup_gui(self):
        """ Create the GUI. """
        self.root = tk.Tk()
        self.root.withdraw()  
        self.center_window(700, 500)
        self.setup_components()
        self.nick_name = self.get_name()
        self.set_title(self.nick_name)
        self.root.deiconify()

    def center_window(self, width, height):
        """ Center the window on the screen. """
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def get_name(self):
        """ Prompt the user for a nickname. """
        while True:
            name = simpledialog.askstring("Name", "Enter your name: ")
            if name:
                return name
            messagebox.showwarning("Warning", "Name can't be empty.")

    def set_title(self, nick_name):
        """ Set the title of the window. """
        self.root.title("Chat - " + nick_name)

    def setup_components(self):
        """ Create the GUI components. """
        self.chat_text = tk.Text(self.root, padx=5, pady=5)
        self.chat_text.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.option_container = tk.Frame(self.root)
        self.option_container.pack(side=tk.BOTTOM, fill=tk.X)

        self.entry_ip = tk.Entry(self.option_container)
        # self.entry_ip.insert(0, self.group)
        self.entry_ip.pack(side=tk.LEFT, padx=10, pady=5)

        self.entry_port = tk.Entry(self.option_container)
        # self.entry_port.insert(0, self.port)
        self.entry_port.pack(side=tk.LEFT, padx=5, pady=5)

        self.broadcast_button = tk.Button(self.option_container, text="Broadcast", command=self.broadcast)
        self.broadcast_button.pack(side=tk.RIGHT, padx=5, pady=5)

        self.join_button = tk.Button(self.option_container, text="Join", command=self.join_group)
        self.join_button.pack(side=tk.RIGHT, padx=5, pady=5)

        self.leave_button = tk.Button(self.option_container, text="Leave", command=self.leave_group, state=tk.DISABLED)
        self.leave_button.pack(side=tk.RIGHT, padx=5, pady=5)

        self.quit_button = tk.Button(self.option_container, text="Quit", command=self.quit_app)
        self.quit_button.pack(side=tk.RIGHT, padx=5, pady=5)

        self.entry_message = tk.Entry(self.root)
        self.entry_message.pack(side=tk.TOP, fill=tk.X, expand=True, padx=5, pady=(5, 0))
        self.entry_message.bind("<Return>", self.send_message)

    def broadcast(self):
        """ Broadcast the message. """
        pass

    def join_group(self):
        """ Join the multicast group. """
        group = self.entry_ip.get()
        port = int(self.entry_port.get())
        self.sock.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(group) + socket.inet_aton(BROADCAST_ADDR))
        self.sock.sendto(self.nick_name.encode(), (group, port))
        self.joined = True
        self.join_button.config(state=tk.DISABLED)
        self.leave_button.config(state=tk.NORMAL)

    def join_multicast_group(self):
        """ Join the multicast group. """
        pass

    def set_ip_and_port(self, state=True):
        """ Enable or disable IP and port entry fields. """
        pass

    def leave_group(self):
        """ Leave the multicast group properly. """
        pass

    def quit_app(self):
        """ Quit the application. """
        pass

    def add_message(self, msg):
        """ Add a message to the chat window. """
        pass

    def receive_message(self):
        """ Receive the message """
        pass

    def send_message(self, mode="broadcast", type="message", content=""):
        """ Send a message over multicast or broadcast. """
        pass
    
    def create_message(self, type, content):
        """ Create a JSON-encoded message. """
        pass
    
    def run(self):
        """ Run the application. """
        threading.Thread(target=self.receive_message, daemon=True).start()
        self.root.mainloop()

if __name__ == "__main__":
    multicast = Multicast()
    multicast.run()
