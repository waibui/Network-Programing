import socket
import tkinter as tk
from tkinter import messagebox

def connect_to_server():
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('127.0.0.1', 9999))
        print("Connected to server")
        return client
    except Exception as e:
        messagebox.showerror("Connection Error", f"Cannot connect to server: {str(e)}")
        root.quit()
        return None

def send_data():
    a = entry_a.get()
    b = entry_b.get()
    operator = entry_operator.get()

    if not (a and b and operator):
        messagebox.showerror("Error", "Please enter all fields")
        return

    try:
        a, b = float(a), float(b)
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers")
        return

    if operator not in ['+', '-', '*', '/']:
        messagebox.showerror("Error", "Please enter a valid operator")
        return

    message = f'{a} {b} {operator}'
    try:
        client.send(message.encode())
        result = client.recv(1024).decode()
        messagebox.showinfo("Result", f"{result}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def on_closing():
    if client:
        client.send("exit".encode())
        client.close()
    root.destroy()

root = tk.Tk()
root.title("Client")

frame = tk.Frame(root)
frame.pack(pady=20, padx=20)

tk.Label(frame, text="Enter The First Number:").grid(row=0, column=0)
entry_a = tk.Entry(frame)
entry_a.grid(row=0, column=1)

tk.Label(frame, text="Enter The Second Number:").grid(row=1, column=0)
entry_b = tk.Entry(frame)
entry_b.grid(row=1, column=1)

tk.Label(frame, text="Enter The Operator (+ - * / ): ").grid(row=2, column=0)
entry_operator = tk.Entry(frame)
entry_operator.grid(row=2, column=1)

btn_send = tk.Button(frame, text="Calculate", command=send_data)
btn_send.grid(row=3, columnspan=2, pady=20)

client = connect_to_server()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
