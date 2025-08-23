# server_ecdh_chat.py
import socket
import threading
import os
import struct
import hashlib

# --- Cryptography primitives (ECDH X25519 + HKDF + AES-GCM) ---
from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# ========== Packet helpers (length-prefixed binary frames) ==========
def send_packet(conn, payload: bytes):
    """
    Send a single message frame: [4-byte big-endian length][payload].
    This prevents TCP stream fragmentation from breaking messages.
    """
    conn.sendall(struct.pack(">I", len(payload)) + payload)

def recv_exactly(conn, n: int) -> bytes:
    """Read exactly n bytes or raise ConnectionError if the socket closes early."""
    chunks = []
    got = 0
    while got < n:
        chunk = conn.recv(n - got)
        if not chunk:
            raise ConnectionError("Socket closed during recv_exactly")
        chunks.append(chunk)
        got += len(chunk)
    return b"".join(chunks)

def recv_packet(conn) -> bytes:
    """
    Receive a single length-prefixed payload.
    First read 4 bytes for the length, then read that many bytes.
    """
    header = recv_exactly(conn, 4)
    (length,) = struct.unpack(">I", header)
    if length > 10_000_000:
        raise ValueError("Refusing oversized packet")
    return recv_exactly(conn, length)

# ========== AES-GCM helpers ==========
def encrypt_message(key: bytes, plaintext: str) -> bytes:
    """
    AES-GCM with a random 96-bit nonce. Output: nonce(12) | tag(16) | ciphertext.
    """
    nonce = os.urandom(12)
    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce))
    enc = cipher.encryptor()
    ct = enc.update(plaintext.encode("utf-8")) + enc.finalize()
    return nonce + enc.tag + ct

def decrypt_message(key: bytes, blob: bytes) -> str:
    """
    Parse nonce(12) | tag(16) | ciphertext and decrypt.
    """
    if len(blob) < 12 + 16:
        raise ValueError("Ciphertext too short")
    nonce = blob[:12]
    tag = blob[12:28]
    ct = blob[28:]
    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce, tag))
    dec = cipher.decryptor()
    pt = dec.update(ct) + dec.finalize()
    return pt.decode("utf-8")

# ========== Key derivation (ECDH X25519 + HKDF-SHA256) ==========
def derive_key_from_shared(shared: bytes, salt: bytes, info: bytes = b"lan-chat aead key") -> bytes:
    """
    HKDF-SHA256 -> 32-byte AES key. Salt comes from server (random) and is sent to client.
    """
    hkdf = HKDF(algorithm=hashes.SHA256(), length=32, salt=salt, info=info)
    return hkdf.derive(shared)

# ========== Chat server ==========
clients = []  # list of dicts: {conn, addr, username, key}
clients_lock = threading.Lock()

def broadcast(plaintext: str, sender_conn=None):
    """
    Encrypt and send a text message to all connected clients except the sender.
    """
    with clients_lock:
        dead = []
        for c in clients:
            if c["conn"] is sender_conn:
                continue
            try:
                blob = encrypt_message(c["key"], plaintext)
                send_packet(c["conn"], blob)
            except Exception:
                dead.append(c)
        # Clean up dead connections
        for c in dead:
            try:
                c["conn"].close()
            except Exception:
                pass
            clients.remove(c)

def handle_client(conn, addr):
    """
    Per-client thread:
    1) ECDH handshake (X25519) -> per-client AES key
    2) Username enrollment (encrypted)
    3) Receive loop: decrypt and broadcast
    4) Cleanup on disconnect
    """
    # --- 1) ECDH handshake ---
    # Generate server's ephemeral X25519 keypair
    server_priv = x25519.X25519PrivateKey.generate()
    server_pub = server_priv.public_key().public_bytes(
        encoding=None,  # raw 32 bytes when encoding=None with X25519PublicKey
        format=None
    )
    # The above API changed in recent versions; a stable alternative:
    # from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
    # server_pub = server_priv.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)

    from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
    server_pub = server_priv.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)  # 32 bytes

    # Create a random salt for HKDF and send it with our public key
    salt = os.urandom(16)
    try:
        # Send: server_pub (32 bytes), then salt (16 bytes) as two packets
        send_packet(conn, server_pub)
        send_packet(conn, salt)

        # Receive client's 32-byte public key
        client_pub_bytes = recv_packet(conn)
        if len(client_pub_bytes) != 32:
            raise ValueError("Invalid client public key length")

        # Compute shared secret: ECDH(server_priv, client_pub)
        client_pub = x25519.X25519PublicKey.from_public_bytes(client_pub_bytes)
        shared = server_priv.exchange(client_pub)  # 32 random-looking bytes

        # Derive symmetric AES key with HKDF
        key = derive_key_from_shared(shared, salt)

        # --- 2) Username exchange (encrypted) ---
        send_packet(conn, encrypt_message(key, "Enter your username:"))
        username_blob = recv_packet(conn)
        username = decrypt_message(key, username_blob).strip() or f"User{addr[1]}"

        # Add this client to the registry
        with clients_lock:
            clients.append({"conn": conn, "addr": addr, "username": username, "key": key})

        join_msg = f"🔵 {username} joined the chat"
        print(f"{addr} -> {join_msg}")
        broadcast(join_msg, sender_conn=conn)

        # --- 3) Chat receive loop ---
        while True:
            blob = recv_packet(conn)  # encrypted frame
            message = decrypt_message(key, blob)
            print(f"{username}: {message}")
            broadcast(f"{username}: {message}", sender_conn=conn)

    except Exception as e:
        # You can log e for debugging if desired
        pass
    finally:
        # --- 4) Cleanup on disconnect ---
        departed_name = None
        with clients_lock:
            for c in list(clients):
                if c["conn"] is conn:
                    departed_name = c["username"]
                    clients.remove(c)
                    break
        try:
            conn.close()
        except Exception:
            pass
        if departed_name:
            leave_msg = f"🔴 {departed_name} left the chat"
            print(f"{addr} -> {leave_msg}")
            broadcast(leave_msg, sender_conn=None)

def server(host="0.0.0.0", port=5000):
    """
    TCP server:
    - Binds to host:port
    - Accepts clients
    - Spawns a thread per client (handle_client)
    """
    # Create TCP socket (IPv4, stream)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Reuse address so quick restarts don't hit TIME_WAIT
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen()
    print(f"💻 Server listening on {host}:{port}")

    while True:
        conn, addr = sock.accept()  # blocks until a client connects
        print(f"✅ New connection from {addr}")
        t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
        t.start()

if __name__ == "__main__":
    server()
