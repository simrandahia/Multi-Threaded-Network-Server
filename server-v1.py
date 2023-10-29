import selectors
import socket

# need a multi-linked list: 
# Head of this list points to the order in which books are received
# head of book A --> points to book A nodes, head of book B --> points to book B nodes,
# node->next - links to the next element in the shared list.   
# node->book_next - links to the next item in the same book. 
# node->next_frequent_search  (part2) links to the next item that had the search terms
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def appendNode(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        last_node = self.head
        while last_node.next:
            last_node = last_node.next
        last_node.next = new_node

    def print_list(self):
        elements = []
        current_node = self.head
        while current_node:
            elements.append(str(current_node.data))
            current_node= current_node.next
        print(" -> ".join(elements)) # print the whole linked list

    def getlast(self): #print the last node
        last_node=self.head
        while last_node.next:
            last_node=last_node.next
        print("->",last_node.data) 

class EchoNIOServer:
    def __init__(self, address, port):
        self.linked_list = LinkedList()
        self.selector = selectors.DefaultSelector()
        self.listen_address = (address, port)
        self.first_line_received = False
        self.client_address=[]

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
            self.client_address=client_address[1]
            print(f"Connected to: {client_address}")
            self.first_line_received = False
            client_socket.setblocking(False)
            self.selector.register(client_socket, selectors.EVENT_READ, data=b'')
        except socket.error as e:
            print(f"Socket error: {e}")

    def service_connection(self, key, mask):
         
        sock = key.fileobj
        if mask & selectors.EVENT_READ:
            data = sock.recv(1024)
            if data:
                print(f"Got: {self.client_address,data.decode()}")
                self.linked_list.appendNode(data.decode())
                self.linked_list.getlast()
            else:
                print(f"Connection closed by client: {sock.getpeername()}")
                self.selector.unregister(sock)
                sock.close()

if __name__ == '__main__':
    server = EchoNIOServer('localhost', 9093)
    server.start_server()
