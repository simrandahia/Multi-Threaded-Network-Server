import selectors
import socket

class EchoNIOServer:
    
    def __init__(self, address, port):
        self.selector = selectors.DefaultSelector()
        self.listen_address = (address, port)
        self.first_line_received = False

    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(self.listen_address)
        server_socket.listen(5)
        server_socket.setblocking(False)
        self.selector.register(server_socket, selectors.EVENT_READ, data=None)
        print(f"Server started on port >> {self.listen_address[1]}")
        print(f"addressName:{self.listen_address[0]}")

        while True:
            events = self.selector.select(timeout=None)
            for key, mask in events:
                # print("\nTEST 1: ", key, "\n")
                # print("\nData in key: ", key.data, "\n")
                
                if key.data is None:
                    self.accept_connection(key.fileobj)
                else:
                    self.service_connection(key, mask)
                    # print("Service conn called")

    def accept_connection(self, server_socket):
        try:
            client_socket, client_address = server_socket.accept()
            print(f"Connected to: {client_address}")
            self.first_line_received = False       # THISSS
            client_socket.setblocking(False)
            self.selector.register(client_socket, selectors.EVENT_READ, data=b'')
        except socket.error as e:
            print(f"Socket error: {e}")

    def service_connection(self, key, mask):
        data = key.fileobj.recv(1024)
        if data:
            # data_decoded = str(data, 'utf-8')
            try:
                data_decoded = data.decode('utf-8')
            except UnicodeDecodeError as e:
                print(f"Error decoding data: {e}")
            # print("\n\nFIRST LINE: ", self.first_line_received, "\n\n")
            if not self.first_line_received:
                self.first_line_received = True
                print(f"Got: {data_decoded.splitlines()[0]}")
                # self.first_line_received = False
            # else:
                # print("YAHOOOO")
        else:
            print(f"Connection closed by client: {key.fileobj.getpeername()}")
            self.selector.unregister(key.fileobj)
            key.fileobj.close()

if __name__ == '__main__':
    server = EchoNIOServer('localhost', 9093)
    server.start_server()
