import socket
import threading

def handle_receive(sock):
    """
    Thread function to receive messages from the server.
    Runs forever until the server closes the connection.
    """
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                print("❌ Disconnected from server.")
                break
            print("\n" + data.decode())  # show incoming message
        except:
            break

def handle_send(sock):
    """
    Thread function to send messages to the server.
    Runs forever until you quit.
    """
    while True:
        try:
            msg = input()
            sock.sendall(msg.encode())
        except:
            break

def client(server_ip, port=5000):
    """
    Connect to the chat server.
    """
    # Create a TCP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server’s IP and port
    sock.connect((server_ip, port))
    print(f"✅ Connected to server {server_ip}:{port}")

    # Start a thread for receiving messages
    threading.Thread(target=handle_receive, args=(sock,), daemon=True).start()

    # Start a thread for sending messages
    threading.Thread(target=handle_send, args=(sock,), daemon=True).start()

    # Keep client running
    while True:
        pass

if __name__ == "__main__":
    # Replace with your server's LAN IP
    server_ip = "0.0.0.0"
    if server_ip == "0.0.0.0":
        server_ip = input("Server LAN IP: ")

    client(server_ip)
