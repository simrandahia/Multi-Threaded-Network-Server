# works on 9pm 29/oct/23
import argparse
import selectors
import socket
import threading
# Reference: 
# https://medium.com/coderscorner/tale-of-client-server-and-socket-a6ef54a74763
# https://github.com/arukshani/JavaIOAndNIO/blob/master/src/com/ruk/blocking/io/EchoIOServer.java

COUNT = 0

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.book_next=None

class Book:
    def __init__(self, name):
        self.name = name
        self.content_head=None
        self.content_tail=None
    def add_line(self, line):
        new_node = Node(line)
        if self.content_head is None:
            self.content_head = new_node
            self.content_tail=new_node
        else:
            self.content_tail.next=new_node
            self.content_tail=new_node

    def display_content(self):
        current=self.content_head
        while current:
            print(f"",self.name,current.data)
            current=current.next

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

    def appendNode(self, data):
        self.received_data.append(data)

    def printBook(self):
        for data in self.received_data:
            print(f"Received Book: {data.name}")




class Non_blocking_server:
    def __init__(self, address, port):
        self.linked_list = LinkedList()
        self.selector = selectors.DefaultSelector()
        self.listen_address = (address, port)
        self.books = []
        self.new_book=[]

    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(self.listen_address)
        server_socket.listen(5)
        server_socket.setblocking(False)
        self.selector.register(server_socket, selectors.EVENT_READ, data=None)
        #to determine the netcat network 
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
            client_socket.setblocking(False)
            self.selector.register(client_socket, selectors.EVENT_READ, data=b'')
            self.new_book = Book(f"book_0{len(self.books) + 1}")
            self.books.append(self.new_book)
            threading.Thread(target=self.service_connection, args=(client_socket, self.new_book)).start()
        except socket.error as e:      
            print(f"Socket error: {e}")

    def service_connection(self, key, mask):
        sock = key.fileobj
        if mask & selectors.EVENT_READ:
            data = sock.recv(1024)
            if data:
                try:
                    decoded_data = data.decode('utf-8')
                    book=self.books[-1]
                    book_name = book.name
                    book.add_line(decoded_data)
                    book.display_content()
                    self.linked_list.appendNode(book)
                    self.linked_list.printBook()
                    with open(f"{book_name}.txt", "a") as file:
                        file.write(decoded_data)
                except UnicodeDecodeError as e:
                    print(f"Error decoding data: {e}")
            else:
                print(f"Connection closed by client: {sock.getpeername()}")
                self.selector.unregister(sock)
                sock.close()

     
    
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description="Echo Server")
    parser.add_argument('-l', '--listen', type=int, default=9093, help='Port number to listen on')
    parser.add_argument('-p', '--param', type=str, default="happy", help='Parameter -p')
    args = parser.parse_args()

    server = Non_blocking_server('localhost', args.listen)  # Use the specified port
    server.start_server()