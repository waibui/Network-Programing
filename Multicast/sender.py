import socket
import time
import tkinter as tk
from threading import Thread

def multicast_send(sock, message):
    multicast_group = ('224.1.1.1', 5007)
    sock.sendto(message.encode(), multicast_group)

def start_sending(sock, entry, status_label):
    while True:
        message = entry.get()
        multicast_send(sock, message)
        status_label.config(text=f"Sent: {message}")
        time.sleep(1)

def start_gui_sender():
    # Tạo socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

    # Tạo GUI
    window = tk.Tk()
    window.title("Multicast Sender")
    
    tk.Label(window, text="Message:").pack()
    entry = tk.Entry(window)
    entry.pack()

    status_label = tk.Label(window, text="")
    status_label.pack()

    # Thread gửi thông điệp
    send_thread = Thread(target=start_sending, args=(sock, entry, status_label), daemon=True)
    send_thread.start()

    window.mainloop()

if __name__ == "__main__":
    start_gui_sender()
