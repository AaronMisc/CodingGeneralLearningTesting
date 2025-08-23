import socket
import threading

# Store all connected clients as (connection, address, username)
clients = []

def broadcast(message, sender_conn=None):
    """
    Send a message to all clients.
    If sender_conn is provided, don't send the message back to them.
    """
    for conn, addr, username in clients:
        if conn != sender_conn:  # don't echo back to the sender
            try:
                conn.sendall(message.encode())
            except:
                # If sending fails, remove this client
                conn.close()
                clients.remove((conn, addr, username))

def handle_client(conn, addr):
    """
    Handle communication with a single client in its own thread.
    """
    try:
        # Step 1: Ask for username
        conn.sendall("Enter your username: ".encode())
        username = conn.recv(1024).decode().strip()
        if not username:
            username = f"User{addr[1]}"  # fallback to something like "User50512"

        # Add this client to the list
        clients.append((conn, addr, username))

        # Announce to everyone
        join_msg = f"🔵 {username} has joined the chat!"
        print(join_msg)
        broadcast(join_msg, sender_conn=conn)

        # Step 2: Chat loop
        while True:
            data = conn.recv(1024)
            if not data:
                break  # client disconnected

            message = data.decode().strip()
            print(f"{username}: {message}")

            # Broadcast to everyone else
            broadcast(f"{username}: {message}", sender_conn=conn)

    except:
        pass
    finally:
        # Remove the client when they leave
        for c in clients:
            if c[0] == conn:
                clients.remove(c)
                leave_msg = f"🔴 {c[2]} has left the chat."
                print(leave_msg)
                broadcast(leave_msg, sender_conn=conn)
                break
        conn.close()

def server(host="0.0.0.0", port=5000):
    """
    Start the chat server.
    """
    # Create a TCP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind it to an IP and port
    sock.bind((host, port))

    # Listen for incoming connections (max 5 waiting in queue)
    sock.listen(5)
    print(f"💻 Server listening on {host}:{port}")

    while True:
        # Accept a new client connection
        conn, addr = sock.accept()
        print(f"✅ New connection from {addr}")

        # Start a new thread for this client
        thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
        thread.start()

if __name__ == "__main__":
    server()
