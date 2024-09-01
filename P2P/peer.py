import socket
import threading
import pickle
import tkinter as tk
from tkinter import scrolledtext, simpledialog, Listbox, END

class Peer:
    def __init__(self,nickname ,ip_server="127.0.0.1", port_server=5555):
        self.nickname = nickname
        self.ip_server = ip_server
        self.port_server = port_server
        self.peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.peer_socket.bind(("0.0.0.0", 0))
        self.ip, self.port = self.peer_socket.getsockname()
        self.chatters = []
        self.running = True
        
        self.setup_gui()
        self.setup_connection()
        
    def setup_gui(self):
        """Set up the GUI."""
        self.root = tk.Tk()
        self.root.title(f"{self.nickname.upper()}: {self.ip}:{self.port}")
        
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(
            padx=10,pady=10,fill=tk.BOTH,expand=True
        )
        
        self.chat_display = scrolledtext.ScrolledText(
            self.main_frame,wrap=tk.WORD, state="disabled"
        )
        self.chat_display.pack(
            side=tk.LEFT,fill=tk.BOTH,expand=True
        )
        
        self.chatter_list = Listbox(self.main_frame)
        self.chatter_list.pack(
            side=tk.RIGHT,fill=tk.BOTH,expand=True
        )
        
        self.message_entry = tk.Entry(self.root)
        self.message_entry.pack(
            padx=10,pady=(0,10),fill=tk.X, side=tk.LEFT,expand=True
        )
        self.message_entry.bind("<Return>", self.send_message)
        
        self.button_send = tk.Button(
            self.root, text="Send", command=self.send_message
        )
        self.button_send.pack(
            padx=10,pady=(0,10),side=tk.RIGHT
        )
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def setup_connection(self):
        """Connect to the server."""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.connect((self.ip_server, self.port_server))
        self.login()
        
    def login(self):
        """Login to the server."""
        self.server_socket.send(
            pickle.dumps(
                {
                    "action": "login",
                    "nickname": self.nickname,
                    "ip": self.ip,
                    "port": self.port
                }
            )
        )
        message = self.server_socket.recv(1024)
        data = pickle.loads(message)
        if isinstance(data, dict) and data.get("exist"):
            print("Nickname already in use. Please try again.")
            self.root.destroy()  
            return
        self.chatters = data
        self.update_chatter_list()
        self.listen_for_peers()
        
    def update_chatter_list(self):
        self.chatter_list.delete(0, END)
        for chatter in self.chatters:
            if chatter["nickname"] != self.nickname:
                self.chatter_list.insert(END, chatter["nickname"]+" "+chatter["ip"]+" "+str(chatter["port"]))
            
    def listen_for_peers(self):
        threading.Thread(target=self.listen_for_messages, daemon=True).start()
        self.root.mainloop()

    def listen_for_messages(self):
        self.peer_socket.listen(5)
        while self.running:
            try:
                conn, _ = self.peer_socket.accept()
                message = conn.recv(1024)
                data = pickle.loads(message)
                if data["action"] == "add":
                    new_chatter = data["chatter"]
                    self.chatters.append(new_chatter)
                    self.add_message(f"{new_chatter['nickname']} has joined the chat.")
                    self.update_chatter_list()
                elif data["action"] == "remove":
                    self.chatters = [
                        chatter
                        for chatter in self.chatters
                        if chatter["nickname"] != data["chatter"]["nickname"]
                    ]
                    self.add_message(f"{data['chatter']['nickname']} has left the chat.")
                    self.update_chatter_list()
                elif data["action"] == "message":
                    self.add_message(f"{data['nickname']}: {data['message']}")
            except OSError:
                break  
            
    def add_message(self, message):
        self.chat_display.configure(state="normal")
        self.chat_display.insert(END, message + "\n")
        self.chat_display.configure(state="disabled")
        self.chat_display.see(END)
        
    def send_message(self, event=None):
        message = self.message_entry.get()
        if message:
            selected_chatter = self.chatter_list.get(tk.ACTIVE)
            if selected_chatter:
                arr = selected_chatter.split(" ")
                nickname = arr[0]
                ip = arr[1]
                port = int(arr[2])
                self.message_entry.delete(0, END)
                peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                peer_socket.connect((ip, port))
                peer_socket.send(
                    pickle.dumps(
                        {
                            "action": "message",
                            "nickname": self.nickname,
                            "message": message
                        }
                    )
                )
                self.add_message(f"You ==> {nickname}: {message}")
                peer_socket.close()
    
    def on_closing(self):
        self.running = False
        self.root.destroy()
        self.logout()
        exit(0)
        
    def logout(self):
        self.server_socket.send(
            pickle.dumps(
                {
                    "action": "logout",
                    "nickname": self.nickname
                }
            )
        )

    
if __name__ == "__main__":
    nickname = simpledialog.askstring("Nickname", "Enter your nickname: ")
    peer = Peer(nickname)