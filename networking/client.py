import socket

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 9999))
    
    print("Sending request to server...")
    request = "Client request"
    client_socket.sendall(request.encode('utf-8'))
    
    response = client_socket.recv(1024)
    print(f"Received response from server: {response.decode('utf-8')}")
    
    client_socket.close()

if __name__ == "__main__":
    start_client()
