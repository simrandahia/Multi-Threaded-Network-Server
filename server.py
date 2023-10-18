import socket

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_socket.bind(('localhost', 12345))

# Listen for incoming connections
server_socket.listen(5)

print("Server is listening for connections...")

while True:
    # Accept a new connection
    client_socket, address = server_socket.accept()
    print(f"Connection from {address} has been established!")

    # Send data to the client
    client_socket.send("Hello, client! Thank you for connecting.".encode('utf-8'))

    # Close the client socket
    client_socket.close()
