import socket
import time
import threading

class TestClient:
    def start_client(self):
        host_address = ('localhost', 9093)
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(host_address)
        print("Client... started")

        thread_name = threading.current_thread().getName()

        # Send messages to server
        messages = [f"{thread_name}: msg1", f"{thread_name}: msg2", f"{thread_name}: msg3"]

        for message in messages:
            buffer = message.encode()
            client.sendall(buffer)
            print(message)
            time.sleep(5)
        client.close()

def run_client():
    try:
        TestClient().start_client()
    except Exception as e:
        print(e)

if __name__ == '__main__':
    client = threading.Thread(target=run_client, name="client-A")
    client.start()
    client_b = threading.Thread(target=run_client, name="client-B")
    client_b.start()
