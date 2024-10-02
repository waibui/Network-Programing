import socket
import tkinter as tk
from threading import Thread

def join_multicast_group(sock, multicast_group):
    group = socket.inet_aton(multicast_group)
    mreq = group + socket.inet_aton('0.0.0.0')
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    return mreq

def leave_multicast_group(sock, mreq):
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_DROP_MEMBERSHIP, mreq)

def multicast_receive(sock, status_label):
    while True:
        data, addr = sock.recvfrom(1024)
        status_label.config(text=f"Received {data.decode()} from {addr}")

def start_receiving(sock, status_label):
    receive_thread = Thread(target=multicast_receive, args=(sock, status_label), daemon=True)
    receive_thread.start()

def start_gui_receiver():
    window = tk.Tk()
    window.title("Multicast Receiver")

    status_label = tk.Label(window, text="Click Join to start listening...")
    status_label.pack()

    # Tạo socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', 5007))
    
    multicast_group = '224.1.1.1'
    mreq = None

    def join():
        nonlocal mreq
        if mreq is None:
            mreq = join_multicast_group(sock, multicast_group)
            status_label.config(text="Joined multicast group, listening...")
            start_receiving(sock, status_label)

    def leave():
        nonlocal mreq
        if mreq is not None:
            leave_multicast_group(sock, mreq)
            status_label.config(text="Left multicast group.")
            mreq = None
            start_receiving(sock, status_label)

    # Nút Join
    join_button = tk.Button(window, text="Join", command=join)
    join_button.pack()

    # Nút Leave
    leave_button = tk.Button(window, text="Leave", command=leave)
    leave_button.pack()

    window.mainloop()

if __name__ == "__main__":
    start_gui_receiver()
