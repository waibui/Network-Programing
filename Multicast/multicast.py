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
        self.gui()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        
    def gui(self):
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
        pass
    
    def join_group(self):
        self.sock.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(MCAST_GRP))
    
    def leave_group(self):
        pass
    
    def quit_app(self):
        pass
    
    def send_message(self, event=None):
        pass
        
    def run(self):
        """ Run the application. """
        # threading.Thread(target=self.receive_message, daemon=True).start()
        self.root.mainloop()
        
if __name__ == "__main__":
    Multicast().run()