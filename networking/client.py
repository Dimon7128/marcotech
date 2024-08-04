import socket
import time

def start_client():
    for i in range(2):  # Loop to connect twice
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 9999))
        
        print(f"Sending large data to server, attempt {i+1}...")
        large_data = b"A" * 70000  # Data larger than typical window size
        bytes_sent = 0
        try:
            while bytes_sent < len(large_data):
                sent = client_socket.send(large_data[bytes_sent:bytes_sent + 1024])
                bytes_sent += sent
                print(f"Bytes sent: {bytes_sent}")
                
                # Simulate client checking if server is still listening
                if bytes_sent % 16384 == 0:
                    print("Client is checking if the server is still listening...")
                    time.sleep(2)  # Short delay before attempting to send more data

            # Wait for server's response
            response = client_socket.recv(1024)
            print(f"Received from server: {response.decode('utf-8')}")
            
            # Send acknowledgment to the server
            ack = "Yes, I'm still listening"
            client_socket.sendall(ack.encode('utf-8'))

            # Receive the final response from the server
            final_response = client_socket.recv(1024)
            print(f"Received final response from server, attempt {i+1}: {final_response.decode('utf-8')}")

        except Exception as e:
            print(f"Exception: {e}")

        client_socket.close()
        
        if i == 0:
            print("Waiting 5 seconds before next attempt...")
            time.sleep(5)  # Optional delay between connections

if __name__ == "__main__":
    start_client()
