import socket

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the server's IP address and port
server_address = ('localhost', 12345)

# Connect to the server
client_socket.connect(server_address)

# Receive data from the server
received_data = client_socket.recv(1024)

# Decode and print the received data
print(received_data.decode('utf-8'))

# Close the socket
client_socket.close()
