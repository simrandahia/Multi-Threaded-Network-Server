import socket
import threading

# Shared data structure to store book data
shared_list = []

# Lock for thread safety
shared_list_lock = threading.Lock()

# Function to handle client connections
def handle_client(client_socket, book_number):
    book_data = []
    while True:
        data = client_socket.recv(4096)
        if not data:
            break
        book_data.append(data)

    with shared_list_lock:
        shared_list.append((book_number, b''.join(book_data)))

    client_socket.close()

# Function for multithreaded analysis (part 2)
def analyze_books(search_pattern):
    while True:
        # Implement your analysis logic here
        pass

# Create a server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 1234))
server.listen(5)

print("Server listening on port 1234")

book_number = 1

# Start the analysis thread
search_pattern = "happy"  # Change this to your desired search pattern
analysis_thread = threading.Thread(target=analyze_books, args=(search_pattern,))
analysis_thread.start()

while True:
    client, addr = server.accept()
    print(f"Accepted connection from {addr}")

    client_handler = threading.Thread(target=handle_client, args=(client, book_number))
    book_number += 1
    client_handler.start()
