import socket
import threading
import tkinter as tk
from tkinter import font

class ClientTime:
    def __init__(self, server_host='127.0.0.1', server_port=5555):
        self.__host = server_host
        self.__port = server_port
        self.server_time = 'Waiting for server...'
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_paused = False
        self.setup_gui()

    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title('Client Time')
        self.root.geometry('300x200')
        self.root.configure(bg='black')

        self.label = tk.Label(self.root, text='Client Time', font=('Helvetica', 16, 'bold'), bg='black', fg='white')
        self.label.pack(side=tk.TOP, pady=10)

        self.time_container = tk.Label(self.root, text=f'[Time]: {self.server_time}', font=('Helvetica', 24), bg='black', fg='lime')
        self.time_container.pack(expand=True)

        self.pause_button = tk.Button(self.root, text='Pause', command=self.pause_connection, font=('Helvetica', 12, 'bold'), bg='red', fg='white')
        self.pause_button.pack(side=tk.LEFT, padx=10)

        self.resume_button = tk.Button(self.root, text='Resume', command=self.resume_connection, font=('Helvetica', 12, 'bold'), bg='green', fg='white')
        self.resume_button.pack(side=tk.RIGHT, padx=10)

        self.root.protocol("WM_DELETE_WINDOW", self.close_connection)

    def close_connection(self):
        try:
            self.server_socket.send('logout'.encode('utf-8'))
        except Exception as e:
            print(f'[Error sending logout]: {e}')
        finally:
            self.server_socket.close()
            self.root.destroy()


    def pause_connection(self):
        if not self.is_paused:
            try:
                self.server_socket.send('pause'.encode('utf-8'))
                self.is_paused = True
                print('[Paused]')
            except Exception as e:
                print(f'[Error sending pause]: {e}')

    def resume_connection(self):
        if self.is_paused:
            try:
                self.server_socket.send('resume'.encode('utf-8'))
                self.is_paused = False
                print('[Resumed]')
            except Exception as e:
                print(f'[Error sending resume]: {e}')

    def run(self):
        try:
            print(f'[Connecting To Server]: {self.__host}:{self.__port}')
            self.server_socket.connect((self.__host, self.__port))
            threading.Thread(target=self.get_time_from_server, daemon=True).start()
            self.root.mainloop()
        except Exception as e:
            print(f'[Error]: {e}')

    def get_time_from_server(self):
        while True:
            try:
                server_time = self.server_socket.recv(1024).decode('utf-8')
                if server_time == 'Server shutting down':
                    print('[Server shutting down]')
                    break
                self.time_container.config(text=f'[Time]: {server_time}')
                print(f'[Time]: {server_time}')
            except Exception as e:
                print(f'[Error receiving time]: {e}')
                break
        self.close_connection()

    @property
    def host(self):
        return self.__host

    @host.setter
    def host(self, value):
        self.__host = value

    @property
    def port(self):
        return self.__port

    @port.setter
    def port(self, value):
        self.__port = value


if __name__ == '__main__':
    client = ClientTime()
    client.run()
