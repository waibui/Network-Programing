import socket
import threading
import tkinter as tk
from tkinter import messagebox, simpledialog

class Multicast:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('', 5007))
        self.mreq = None
        self.setup_gui()

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
        self.entry_ip.insert(0, '224.1.1.1')
        self.entry_ip.pack(side=tk.LEFT, padx=10, pady=5)

        self.entry_port = tk.Entry(self.option_container)
        self.entry_port.insert(0, 5007)
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
        if self.mreq is None:
            self.mreq = self.join_multicast_group(group)  # Pass group IP
            self.receive_message(self.sock)

        self.joined = True
        self.join_button.config(state=tk.DISABLED)
        self.leave_button.config(state=tk.NORMAL)

    def join_multicast_group(self, group):
        """ Join the multicast group. """
        group = socket.inet_aton(group)
        mreq = group + socket.inet_aton('0.0.0.0')
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        return mreq

    def set_ip_and_port(self, state=True):
        """ Enable or disable IP and port entry fields. """
        pass

    def leave_group(self):
        """ Leave the multicast group properly. """
        if self.mreq is not None:
            self.leave_multicast_group(self.sock, self.mreq)
            self.mreq = None
            self.join_button.config(state=tk.NORMAL)
            self.leave_button.config(state=tk.DISABLED)

    def leave_multicast_group(self, sock, mreq):
        """ Leave the multicast group. """
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_DROP_MEMBERSHIP, mreq)

    def quit_app(self):
        """ Quit the application. """
        self.root.quit()
        self.sock.close()

    def add_message(self, msg):
        """ Add a message to the chat window. """
        self.chat_text.insert(tk.END, msg + '\n')

    def receive_message(self, sock):
        """ Receive the message in a separate thread. """
        threading.Thread(target=self.multicast_receive, args=(sock,), daemon=True).start()

    def multicast_receive(self, sock):
        """ Handle receiving multicast messages. """
        while True:
            try:
                data, addr = sock.recvfrom(1024)
                self.add_message(data.decode())
            except OSError:
                break  # Handle socket close or leave group properly

    def send_message(self, event=None):
        """ Send a message over multicast. """
        group = self.entry_ip.get()
        port = int(self.entry_port.get())
        message = f"{self.nick_name}: {self.entry_message.get()}"
        self.sock.sendto(message.encode(), (group, port))
        self.entry_message.delete(0, tk.END)

    def run(self):
        """ Run the application. """
        self.root.mainloop()

if __name__ == "__main__":
    multicast = Multicast()
    multicast.run()
