import socket
import threading
import pickle
import sys
import signal
from chatter import Chatter

class Server:
    def __init__(self, ip="127.0.0.1", port=5555):
        self.ip = ip
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.chatters = []
        self.server.bind((self.ip, self.port))
        self.server.listen(5)
        print("Server started on", self.ip, ":", self.port)
        
        signal.signal(signal.SIGINT, self.shutdown)
        
    def shutdown(self, signum, frame):
        print("\nServer off")
        self.server.close()
        sys.exit(0)
    def run(self):
        while True:
            client_socket, _ = self.server.accept()
            threading.Thread(target=self.handler_client, args=(client_socket, self)).start()
            
    def handler_client(self,client_socket, server):
        while True:
            try:
                message = client_socket.recv(1024)
                if message:
                    data = pickle.loads(message)
                    if data["action"] == "login":
                        server.add_chatter(data, client_socket)
                    elif data["action"] == "logout":
                        server.remove_chatter(data)
            except Exception as e:
                print(f"Error handling client - {e}")
                client_socket.close()
                break
    
    def add_chatter(self, data, client_socket):
        nickname = data["nickname"]
        for chatter in self.chatters:
            if chatter.nickname == nickname:
                client_socket.send(
                    pickle.dumps(
                        {
                            "exist": True
                        }
                    )
                )
                client_socket.close()
                return
        new_chatter = Chatter(data["nickname"], data["ip"], data["port"])
        self.chatters.append(new_chatter)
        print(f"{new_chatter.nickname} connected")
    
        client_socket.send(
            pickle.dumps(
                [ch.__dict__ for ch in self.chatters]
            )
        )
        
        for chatter in self.chatters:
            if chatter != new_chatter:
                try:
                    chatter_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    chatter_socket.connect((chatter.ip, chatter.port))
                    chatter_socket.send(
                        pickle.dumps(
                            {
                                "action": "add",
                                "chatter": new_chatter.__dict__
                            }
                        )
                    )
                    chatter_socket.close()
                except Exception as e:
                    print(f"Error sending add message to {chatter.nickname} - {e}")

    def remove_chatter(self, data):
        removed_chatter = None
        for chatter in self.chatters:
            if chatter.nickname == data["nickname"]:
                removed_chatter = chatter
                break
        if removed_chatter:
            self.chatters.remove(removed_chatter)
            print(f"{removed_chatter.nickname} disconnected")
            
            for chatter in self.chatters:
                try:
                    chatter_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    chatter_socket.connect((chatter.ip, chatter.port))
                    chatter_socket.send(
                        pickle.dumps(
                            {
                                "action": "remove",
                                "chatter": removed_chatter.__dict__
                            }
                        )
                    )
                    chatter_socket.close()
                except Exception as e:
                    print(f"Error sending remove message to {chatter.nickname} - {e}")
                    
if __name__ == "__main__":
    server = Server()
    server.run()