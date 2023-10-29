import argparse
import selectors
import socket
import threading

COUNT = 0

class EchoNIOServer:
    def __init__(self, address, port):
        self.selector = selectors.DefaultSelector()
        self.listen_address = (address, port)
        self.lock = threading.Lock()
        self.connection_queue = []

    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(self.listen_address)
        server_socket.listen(5)
        server_socket.setblocking(False)
        self.selector.register(server_socket, selectors.EVENT_READ, data=None)
        print(f"Server started on port >> {self.listen_address[1]}")
        print(f"addressName: {self.listen_address[0]}")

        # Start a thread to handle incoming connections
        connection_thread = threading.Thread(target=self.handle_connections)
        connection_thread.daemon = True
        connection_thread.start()

        while True:
            events = self.selector.select(timeout=None)
            for key, mask in events:
                if key.data is None:
                    self.accept_connection(key.fileobj)
                else:
                    self.service_connection(key, mask)

    def accept_connection(self, server_socket):
        try:
            client_socket, client_address = server_socket.accept()
            print(f"Connected to: {client_address}")
            self.connection_queue.append(client_socket)
        except socket.error as e:
            print(f"Socket error: {e}")

    def handle_connections(self):
        global COUNT
        while True:
            if self.connection_queue:
                client_socket = self.connection_queue.pop(0)
                COUNT += 1
                self.service_connection(client_socket)

    def service_connection(self, sock):
        print("service_connection method is called")
        data = sock.recv(1024)
        if data:            
            book_name = self.determine_book_name()
            print(f"Working on writing to the {book_name} file")
            with self.lock:
                decoded_data = data.decode('utf-8')
                # print(f"Got: {decoded_data}")
                self.save_to_book(book_name, decoded_data)
        else:
            print(f"Connection closed by client: {sock.getpeername()}")
            sock.close()

    def determine_book_name(self):
        global COUNT
        if COUNT < 10:
            return f"book_0{COUNT}"
        else:
            return f"book_{COUNT}"
    

    def save_to_book(self, name, content):
        # Implement your book-saving logic here
        # You can use the lock to ensure exclusive access to the file
        print("save_to_book method is called")
        file_path = f"{name}.txt"
        print(f"Saving content to {file_path}:")
        print(content)
        with self.lock:
            # Write content to the book file
            with open(f"{name}.txt", "a") as file:
                file.write(content)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Echo Server")
    parser.add_argument('-l', '--listen', type=int, default=9093, help='Port number to listen on')
    parser.add_argument('-p', '--param', type=str, default="happy", help='Parameter -p')
    args = parser.parse_args()

    server = EchoNIOServer('localhost', args.listen)  # Use the specified port
    server.start_server()
