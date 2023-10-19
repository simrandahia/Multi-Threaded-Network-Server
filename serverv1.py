import selectors
import socket
import subprocess

class EchoNIOServer:

    def __init__(self, address, port):
        self.shared_list = []
        self.selector = selectors.DefaultSelector()
        self.listen_address = (address, port)

    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(self.listen_address)
        server_socket.listen(5)
        server_socket.setblocking(False)
        self.selector.register(server_socket, selectors.EVENT_READ, data=None)
        print("Hello")
        print(f"Server started on port >> {self.listen_address[1]}")

        while True:
            events = self.selector.select(timeout=None)
            for key, mask in events:
                if key.data is None:
                    self.accept_connection(key.fileobj)
                else:
                    self.service_connection(key, mask)

    def accept_connection(self, server_socket):
        client_socket, client_address = server_socket.accept()
        print(f"Connected to: {client_address}")
        client_socket.setblocking(False)
        self.selector.register(client_socket, selectors.EVENT_READ, data=b'')

    def service_connection(self, key, mask):
        sock = key.fileobj
        if mask & selectors.EVENT_READ:
            data = sock.recv(1024)
            if data:
                print(f"Got: {data.decode()}")
            else:
                print(f"Connection closed by client: {sock.getpeername()}")
                self.selector.unregister(sock)
                sock.close()

    def process_command(self, command):
        parts = command.split()
        if len(parts) == 5 and parts[0] == 'nc' and parts[1] == 'localhost' and parts[2] == '9093' and parts[3] == '-i':
            try:
                delay = float(parts[4])
                filename = parts[5]
                output = subprocess.check_output(['cat', filename], universal_newlines=True)
                lines = output.split('\n')
                if lines:
                    head_pointer = lines[0]
                    self.shared_list.append(head_pointer)
                    print(f"Added to shared_list: {head_pointer}")
                else:
                    print("File is empty.")
            except (ValueError, subprocess.CalledProcessError, IndexError) as e:
                print(f"Error: {e}")
        else:
            print("Invalid command format.")

if __name__ == '__main__':
    server = EchoNIOServer('localhost', 9093)
    server.start_server()
    # command = "nc localhost 1234 -i 1 filename.txt"
    # print("Hello")
    # server.process_command(command)


# import selectors
# import socket


# class EchoNIOServer:

     
#     def __init__(self, address, port):
#         self.shared_list=[]
#         self.selector = selectors.DefaultSelector()
#         self.listen_address = (address, port)

#     def start_server(self):
#         server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#         server_socket.bind(self.listen_address)
#         server_socket.listen(5)
#         server_socket.setblocking(False)
#         self.selector.register(server_socket, selectors.EVENT_READ, data=None)
#         print(f"Server started on port >> {self.listen_address[1]}")

#         while True:
#             events = self.selector.select(timeout=None)
#             for key, mask in events:
#                 if key.data is None:
#                     self.accept_connection(key.fileobj)
#                 else:
#                     self.service_connection(key, mask)

#     def accept_connection(self, server_socket):
#         client_socket, client_address = server_socket.accept()
#         print(f"Connected to: {client_address}")
#         client_socket.setblocking(False)
#         self.selector.register(client_socket, selectors.EVENT_READ, data=b'')

#     def service_connection(self, key, mask):
#         sock = key.fileobj
#         if mask & selectors.EVENT_READ:
#             data = sock.recv(1024)
#             if data:
#                 print(f"Got: {data.decode()}")
#             else:
#                 print(f"Connection closed by client: {sock.getpeername()}")
#                 self.selector.unregister(sock)
#                 sock.close()

# if __name__ == '__main__':
#     server = EchoNIOServer('localhost', 9093)
#     server.start_server()

