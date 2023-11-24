import argparse
import selectors
import socket
import threading

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.book_next = None
        self.next_frequent_search = None

class Book:
    def __init__(self, name):
        self.name = name
        self.content_head = None
        self.content_tail = None
        self.lock = threading.Lock()

    def add_line(self, line):
        new_node = Node(line)
        if self.content_head is None:
            self.content_head = new_node
            self.content_tail = new_node
        else:
            self.content_tail.next = new_node
            self.content_tail = new_node

    def display_content(self):
        current = self.content_head
        while current:
            print(f"{self.name}: {current.data}")
            current = current.next

    def save_to_file(self):
        with open(f"{self.name}.txt", "w") as file:
            current = self.content_head
            while current:
                file.write(current.data)
                current = current.next
        print(f"{self.name} saved on server")

class LinkedList:
    def __init__(self):
        self.shared_head = None
        self.received_data = []
        self.lock = threading.Lock()

    def appendNode(self, data):
        self.received_data.append(data)

    def printBook(self):
        for data in self.received_data:
            print(f"Received Book: {data.name}")

class NonBlockingServer:
    def __init__(self, address, port):
        self.linked_list = LinkedList()
        self.selector = selectors.DefaultSelector()
        self.listen_address = (address, port)
        self.books = []

    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(self.listen_address)
        server_socket.listen(5)
        server_socket.setblocking(False)
        self.selector.register(server_socket, selectors.EVENT_READ, data=None)
        print(f"Server started on port {self.listen_address[1]}")

        while True:
            events = self.selector.select(timeout=None)
            for key, mask in events:
                if key.data is None:
                    self.accept_connection(key.fileobj)
                else:
                    threading.Thread(target=self.service_connection, args=(key,)).start()

    def accept_connection(self, server_socket):
        try:
            client_socket, client_address = server_socket.accept()
            print(f"Connected to: {client_address}")
            client_socket.setblocking(False)
            new_book = Book(f"book_0{len(self.books) + 1}")
            self.books.append(new_book)
            self.selector.register(client_socket, selectors.EVENT_READ, data=new_book)
            threading.Thread(target=self.service_connection, args=(client_socket,)).start()
        except socket.error as e:
            print(f"Socket error: {e}")

    def service_connection(self, key):
        sock = key.fileobj
        book = key.data

        data = sock.recv(1024)
        if data:
            try:
                decoded_data = data.decode('utf-8')
                with book.lock:
                    book.add_line(decoded_data)
                    book.display_content()
                    with open(f"{book.name}.txt", "a") as file:
                        file.write(decoded_data)
                    new_node = Node(decoded_data)
                    new_node.book_next = book.content_head
                    with self.linked_list.lock:
                        new_node.next = self.linked_list.shared_head
                        self.linked_list.shared_head = new_node
                        new_node.next_frequent_search = self.linked_list.shared_head
                        self.linked_list.shared_head = new_node
                        print(f"Added node to the shared list: {decoded_data}")
            except UnicodeDecodeError as e:
                print(f"Error decoding data: {e}")
        else:
            print(f"Connection closed by client: {sock.getpeername()}")
            self.selector.unregister(sock)
            sock.close()
            self.linked_list.appendNode(book)
            self.linked_list.printBook()
            book.save_to_file()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Echo Server")
    parser.add_argument('-l', '--listen', type=str, default='localhost', help='Address to listen on')
    parser.add_argument('-port', '--port', type=int, default=9093, help='Port number to listen on')
    args = parser.parse_args()

    server = NonBlockingServer(args.listen, args.port)
    server.start_server()
