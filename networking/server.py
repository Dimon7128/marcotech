import socket
import time

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 9999))
    server_socket.listen(1)
    print("Server listening on port 9999...")
    
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr} has been established.")
        
        data_received = 0
        buffer = b""
        try:
            while True:
                part = client_socket.recv(1024)
                if not part:
                    break
                buffer += part
                data_received += len(part)
                print(f"Received data: {data_received} bytes")
                
                # Simulate window full scenario
                if data_received >= 65535:
                    print("Server buffer full, introducing delay...")
                    time.sleep(10)  # Short delay
                    break

            # Send "Are you still listening?" message
            message = "Are you still listening?"
            client_socket.sendall(message.encode('utf-8'))

            # Receive the client's response to the "Are you still listening?" message
            ack = client_socket.recv(1024).decode('utf-8')
            print(f"Received acknowledgment: {ack}")

            # Final response to the client
            final_response = "Server response after delay"
            client_socket.sendall(final_response.encode('utf-8'))

        except Exception as e:
            print(f"Exception: {e}")

        client_socket.close()

if __name__ == "__main__":
    start_server()
