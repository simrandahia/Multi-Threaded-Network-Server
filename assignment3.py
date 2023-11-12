# python3 assignment3.py -l localhost -p "little"
# nc localhost 9093 -i 1 <bookA.txt
# nc localhost 9093 -i 1 <bookB.txt

import argparse
import selectors
import socket
import threading
import time
from collections import Counter

# Reference: 
# https://medium.com/coderscorner/tale-of-client-server-and-socket-a6ef54a74763
# https://github.com/arukshani/JavaIOAndNIO/blob/master/src/com/ruk/blocking/io/EchoIOServer.java

COUNT = 0

class Node:
    def __init__(self, data, book=None):
        self.data = data
        self.next = None
        self.book_next = None
        self.next_frequent_search = None
        self.book = book
class Book:
    def __init__(self, name, port):
        self.name = name
        self.port = port
        self.content_head = None
        self.content_tail = None
        self.lock = threading.Lock()
        
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
            # print(f"",self.name,current.data)
            current=current.next

    def save_to_file(self):
        with open(f"{self.name}.txt", "w") as file:
            current = self.content_head
            while current:
                file.write(current.data)
                current = current.next
        print(f"{self.name} saved on server")

    def update_frequent_searches(self, new_node):
        with self.lock:
            new_node.next_frequent_search = self.content_head
            self.content_head = new_node

class LinkedList:
    def __init__(self):
        self.shared_head = None
        self.received_data = []
        self.lock = threading.Lock()

    def appendNode(self, data):
        with self.lock:
            self.received_data.append(data)

    def printBook(self):
        with self.lock:
            for data in self.received_data:
                print(f"Received Book: {data.name}")

class AnalysisThread(threading.Thread):
    def __init__(self, linked_list, search_pattern, interval):
        super().__init__()
        self.linked_list = linked_list
        self.search_pattern = search_pattern
        self.interval = interval
        self.stop_event = threading.Event()

    def run(self):
        while not self.stop_event.is_set():
            time.sleep(self.interval)
            if self.stop_event.is_set():
                break
            self.analyze_and_print()

    def analyze_and_print(self):
        with self.linked_list.lock:
            current_node = self.linked_list.shared_head.next  # Skip the dummy node
            nodes_with_pattern = []

            while current_node is not None:
                if current_node.data is not None and self.search_pattern in current_node.data:
                    nodes_with_pattern.append(current_node)
                current_node = current_node.next

            title_frequency = Counter([node.book.name for node in nodes_with_pattern if node.book is not None])
            sorted_titles = sorted(title_frequency.items(), key=lambda x: (x[1], x[0]), reverse=True)
            
            # Acquire a lock before printing
            with threading.Lock():
                print(f"\nBooks titles sorted by frequency of search pattern '{self.search_pattern}':")
                for title, frequency in sorted_titles:
                    print(f"{title}: {frequency} occurrences")
                    

def start_analysis_threads(linked_list, search_pattern, interval, num_threads):
    threads = []
    for _ in range(num_threads):
        analysis_thread = AnalysisThread(linked_list, search_pattern, interval)
        analysis_thread.start()
        threads.append(analysis_thread)
    return threads

class Non_blocking_server:
    def __init__(self, address, initial_port, search_pattern, analysis_interval, num_analysis_threads):
        self.linked_list = LinkedList()
        self.selector = selectors.DefaultSelector()
        self.listen_address = (address, initial_port)
        self.books = []
        self.new_book = []
        self.analysis_threads = start_analysis_threads(
            self.linked_list, search_pattern, analysis_interval, num_analysis_threads
        )

    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(self.listen_address)
        server_socket.listen(5)
        server_socket.setblocking(False)
        self.selector.register(server_socket, selectors.EVENT_READ, data=None)

        # Increment port for the next book
        self.listen_address = (self.listen_address[0], self.listen_address[1] + 1)

        print(f"Server started on port >> {self.listen_address[1]}")
        print(f"addressName:{self.listen_address[0]}")

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
            self.selector.register(client_socket, selectors.EVENT_READ, data=b'')

            # Assign a unique port to each book
            new_book_port = self.listen_address[1]
            new_book_name = f"book_{len(self.books) + 1:02d}"
            self.new_book = Book(new_book_name, new_book_port)
            self.books.append(self.new_book)

            threading.Thread(target=self.service_connection, args=(client_socket, self.new_book)).start()
        except socket.error as e:
            print(f"Socket error: {e}")

    def service_connection(self, key, mask):
        sock = key.fileobj
        book = key.data
        if mask & selectors.EVENT_READ:
            data = sock.recv(1024)
            if data:
                try:
                    decoded_data = data.decode('utf-8')
                    with book.lock:
                        book.add_line(decoded_data)
                        book.display_content()
                        with open(f"{book.name}.txt", "a") as file:
                            file.write(decoded_data)
                        new_node = Node(decoded_data, book)
                        new_node.book_next = book.content_head
                        with self.linked_list.lock:
                            new_node.next = self.linked_list.shared_head
                            self.linked_list.shared_head = new_node
                            new_node.next_frequent_search = self.linked_list.shared_head
                            self.linked_list.shared_head = new_node
                            print(f"Added node to the shared list ({book.name}): {decoded_data}")
                except UnicodeDecodeError as e:
                    print(f"Error decoding data: {e}")
            else:
                print(f"Connection closed by client: {sock.getpeername()}")
                self.selector.unregister(sock)
                sock.close()
                self.linked_list.appendNode(book)
                self.linked_list.printBook()
                book.save_to_file()

    def stop_analysis_threads(self):
        for thread in self.analysis_threads:
            thread.stop_event.set()
            thread.join()
    
if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(description="Echo Server")
        parser.add_argument('-l', '--listen', type=int, default=12345, help='Initial port number to listen on')
        parser.add_argument('-p', '--param', type=str, default="happy", help='Parameter -p')
        parser.add_argument('-i', '--interval', type=int, default=5, help='Analysis interval in seconds')
        parser.add_argument('-t', '--num-threads', type=int, default=2, help='Number of analysis threads')
        args = parser.parse_args()

        # Pass the additional parameters to the Non_blocking_server constructor
        server = Non_blocking_server('localhost', args.listen, args.param, args.interval, args.num_threads)
        server.start_server()
        server.stop_analysis_threads()

    except Exception as e:
        print(f"An error occurred: {e}")



