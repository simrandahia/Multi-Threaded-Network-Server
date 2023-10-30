# works on 9pm 29/oct/23
import argparse
import selectors
import socket

COUNT = 1

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.book_next=None

class LinkedList:
    def __init__(self):
        self.head = None

    def appendNode(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            last_node = self.head
            while last_node.next:
                last_node = last_node.next
            last_node.next = new_node

    def print_list(self):
        elements = []
        current_node = self.head
        while current_node:
            elements.append(str(current_node.data))
            current_node = current_node.next
        print(" -> ".join(elements))

    def getlast(self):
        last_node = self.head
        while last_node:
            last_node = last_node.next
        print("->", last_node.data.name)

class Book:
    def __init__(self, name):
        self.name = name
        self.content_head=None
        self.content_tail=None

    def add_line(self, line):
        new_node = Node(line)
        if self.content_head is None:
            self.content_head = new_node
            self.content_tail = new_node
        else:
            self.content_tail.next = new_node
            self.content_tail = new_node

    def display_content(self):
        current=self.content_head
        while current:
            print(f"",self.name,current.data)
            current=current.next

    def save_to_file(self):
        with open(f"{self.name}.txt", "w") as file:
            file.writelines(self.content)
        print(f"{self.name} saved on server")

class EchoNIOServer:
    def __init__(self, address, port):
        self.linked_list = LinkedList()
        self.selector = selectors.DefaultSelector()
        self.listen_address = (address, port)
        self.first_line_received = False
        self.books = []

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
                if key.data is None:
                    self.accept_connection(key.fileobj)
                else:
                    self.service_connection(key, mask)

    def accept_connection(self, server_socket):
        try:
            client_socket, client_address = server_socket.accept()
            print(f"Connected to: {client_address}")
            self.first_line_received = True
            client_socket.setblocking(False)
            self.selector.register(client_socket, selectors.EVENT_READ, data=b'')
        except socket.error as e:      
            print(f"Socket error: {e}")

    def service_connection(self, key, mask):
        sock = key.fileobj
        if mask & selectors.EVENT_READ:
            data = sock.recv(1024)
            if data:
                # print(f"Got: {data.decode()}")
                # book_name = self.determine_book_name(data.decode())  # Replace with logic to identify book name
                # book = self.get_or_create_book(book_name)
                # book.add_line(data.decode())
                try:
                    decoded_data = data.decode('utf-8')
                    # print(f"Got: {decoded_data}")
                    book_name = self.determine_book_name(decoded_data)
                    book = self.get_or_create_book(book_name)
                    book.add_line(decoded_data)
                    book.display_content()

                    # Save data to a file
                    with open(f"{book_name}.txt", "a") as file:
                        file.write(decoded_data)

                except UnicodeDecodeError as e:
                    # Handle the decoding error gracefully
                    print(f"Error decoding data: {e}")

            else:
                print(f"Connection closed by client: {sock.getpeername()}")
                self.selector.unregister(sock)
                sock.close()

    def determine_book_name(self, data):
        # Implement logic to identify the book name from data
        global COUNT
        # COUNT += 1
        print("Hello1")
        return f"book_0{COUNT}"  

    def get_or_create_book(self, name):
        for book in self.books:
            if book.name == name:
                return book
        new_book = Book(name)
        self.books.append(new_book)
        print("Hello")
        return new_book
    
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description="Echo Server")
    parser.add_argument('-l', '--listen', type=int, default=9093, help='Port number to listen on')
    parser.add_argument('-p', '--param', type=str, default="happy", help='Parameter -p')
    args = parser.parse_args()

    server = EchoNIOServer('localhost', args.listen)  # Use the specified port
    server.start_server()
