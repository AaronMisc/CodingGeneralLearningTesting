# client_ecdh_chat.py
import socket
import threading
import struct
import os
from sys import exit
from time import sleep
from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.shortcuts import print_formatted_text
from prompt_toolkit.formatted_text import FormattedText
from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

USERNAME_COLORS = ["ansired", "ansigreen", "ansiyellow", "ansiblue", "ansimagenta", "ansicyan", "ansibrightred", "ansibrightgreen", "ansibrightblue", "ansibrightmagenta", "ansibrightcyan"]

# ========== Packet helpers ==========
def send_packet(conn, payload: bytes):
    conn.sendall(struct.pack(">I", len(payload)) + payload)

def recv_exactly(conn, n: int) -> bytes:
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
    header = recv_exactly(conn, 4)
    (length,) = struct.unpack(">I", header)
    if length > 10_000_000:
        raise ValueError("Refusing oversized packet")
    return recv_exactly(conn, length)

# ========== Crypto helpers ==========
def derive_key_from_shared(shared: bytes, salt: bytes, info: bytes = b"lan-chat aead key") -> bytes:
    hkdf = HKDF(algorithm=hashes.SHA256(), length=32, salt=salt, info=info)
    return hkdf.derive(shared)

def encrypt_message(key: bytes, plaintext: str) -> bytes:
    nonce = os.urandom(12)
    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce))
    enc = cipher.encryptor()
    ct = enc.update(plaintext.encode("utf-8")) + enc.finalize()
    return nonce + enc.tag + ct

def decrypt_message(key: bytes, blob: bytes) -> str:
    if len(blob) < 28:
        raise ValueError("Ciphertext too short")
    nonce = blob[:12]
    tag = blob[12:28]
    ct = blob[28:]
    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce, tag))
    dec = cipher.decryptor()
    pt = dec.update(ct) + dec.finalize()
    return pt.decode("utf-8")

def get_username_color(name: str) -> str:
    return USERNAME_COLORS[hash(name) % len(USERNAME_COLORS)]

def client(server_ip: str, port: int = 5000):
    session = PromptSession()

    # --- 0) Connect TCP ---
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server_ip, port))
    print(f"✅ Connected to {server_ip}:{port}")

    # --- 1) ECDH handshake (X25519) ---
    # Generate client's ephemeral keypair
    client_priv = x25519.X25519PrivateKey.generate()
    from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
    client_pub_bytes = client_priv.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)  # 32 bytes

    # Receive server public key (32 bytes) and salt (16 bytes)
    server_pub_bytes = recv_packet(sock)
    salt = recv_packet(sock)

    # Send our public key to server
    send_packet(sock, client_pub_bytes)

    # Compute shared secret and derive AES key
    server_pub = x25519.X25519PublicKey.from_public_bytes(server_pub_bytes)
    shared = client_priv.exchange(server_pub)
    key = derive_key_from_shared(shared, salt)
    print("🔑 Secure channel established (ECDH + AES-GCM)")

    # --- 2) Receive username prompt (encrypted), send username ---
    prompt_blob = recv_packet(sock)
    prompt = decrypt_message(key, prompt_blob)
    username = input(prompt + " ").strip() or "Anon"
    send_packet(sock, encrypt_message(key, username))

    # --- 3) Threads: receive and send concurrently ---
    def leave_server():
        sock.close()
        print("\n❌ Disconnected from server.")
        exit()

    def print_user_message(sender: str, content: str):
        sender_style = f"bold {get_username_color(sender)}"
        text = FormattedText([
            (sender_style, sender),
            ("", ":"),
            ("", content),
        ])
        print_formatted_text(text)

    def print_system_message(message: str):
        # Example: underline + white
        text = FormattedText([
            ("underline ansiwhite", message),
        ])
        print_formatted_text(text)


    def recv_loop():
        while True:
            try:
                blob = recv_packet(sock)
                msg = decrypt_message(key, blob)

                if msg.count(":") == 1: # User message
                    sender, content = msg.split(":", 1)
                    print_user_message(sender, content)
                else: # System message
                    print_system_message(msg)
            except Exception:
                break

    def build_prompt_tokens(username: str) -> FormattedText:
        user_style = f"bold {get_username_color(username)}"
        return FormattedText([
            (user_style, username),
            ("", ": "),
        ])


    def send_loop():
        with patch_stdout():
            while True:
                prompt_tokens = build_prompt_tokens(username)
                msg = session.prompt(prompt_tokens).strip()
                if msg in ["/q", "/quit", "/exit", "/bye", "/l", "/leave"]:
                    leave_server()
                    break
                elif msg:
                    send_packet(sock, encrypt_message(key, msg))

    recv_thread = threading.Thread(target=recv_loop)
    send_thread = threading.Thread(target=send_loop)

    recv_thread.start()
    send_thread.start()

    # Keep main thread alive
    try:
        while True:
            if not (recv_thread.is_alive() and send_thread.is_alive()):
                break
            sleep(0.1)
    except:
        sock.close()

if __name__ == "__main__":
    server_ip = "0.0.0.0"
    if server_ip == "0.0.0.0":
        server_ip = input("Server LAN IP: ").strip()

    client(server_ip)  # replace with your server's LAN IP
