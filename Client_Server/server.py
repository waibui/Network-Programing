import socket
import threading

def handle_client(client,address):
    try:
        while True:
            data = client.recv(1024).decode()
            if(data == "exit"):
                print(f'Client {address} disconnected')
                client.close()
                break
            if not data:
                break

            try:
                a, b, operator = data.split()
                a, b = float(a), float(b)
                operations = {
                    '+': a + b,
                    '-': a - b,
                    '*': a * b,
                    '/': a / b if b != 0 else 'Cannot divide by zero'
                }
                result = operations.get(operator, 'Invalid operator')
            except ValueError:
                result = 'Invalid input'
            
            client.send(str(result).encode())
    except Exception as e:
        print(f'Error: {e}')
    finally:
        client.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 9999
    try:
        server.bind(('0.0.0.0', port))
        server.listen(5)
        print(f'Listening on port {port}...')
        while True:
            client, address = server.accept()
            print(f'Connected to {address}')
            threading.Thread(target=handle_client, args=(client,address)).start()
    except KeyboardInterrupt:
        print('Server closed')
    except Exception as e:
        print(f'Error: {e}')
    finally:
        server.close()

if __name__ == '__main__':
    main()
