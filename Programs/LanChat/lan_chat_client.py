#!/usr/bin/env python3
"""
lan_chat_client.py
Terminal-based chat client that performs X25519 DH with other clients
to derive per-peer AES-GCM symmetric keys. All chat messages are encrypted
and the server only relays ciphertexts.
"""

import socket, threading, struct, json, base64, time, sys
from getpass import getpass
from datetime import datetime

# cryptography primitives
from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

SERVER_IP = '192.168.1.100'   # change to server IP
SERVER_PORT = 5001

# Helpers for framed JSON over TCP
def send_json(conn, obj):
    data = json.dumps(obj).encode('utf-8')
    length = struct.pack('>I', len(data))
    conn.sendall(length + data)

def recv_json(conn):
    # read 4-byte length
    raw_len = conn.recv(4)
    if not raw_len:
        return None
    msg_len = struct.unpack('>I', raw_len)[0]
    data = b''
    while len(data) < msg_len:
        chunk = conn.recv(msg_len - len(data))
        if not chunk:
            return None
        data += chunk
    return json.loads(data.decode('utf-8'))

# Crypto helpers
def derive_shared_key(priv: x25519.X25519PrivateKey, peer_pub_bytes: bytes) -> bytes:
    peer_pub = x25519.X25519PublicKey.from_public_bytes(peer_pub_bytes)
    shared = priv.exchange(peer_pub)  # raw shared secret bytes
    # Derive a 32-byte AES key using HKDF-SHA256
    hkdf = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b'lan-chat-aes-key')
    key = hkdf.derive(shared)
    return key  # 32 bytes for AES-256

def encrypt_message(aes_key: bytes, plaintext: bytes):
    aesgcm = AESGCM(aes_key)
    nonce = os.urandom(12)
    ct = aesgcm.encrypt(nonce, plaintext, None)
    return nonce, ct

def decrypt_message(aes_key: bytes, nonce: bytes, ciphertext: bytes):
    aesgcm = AESGCM(aes_key)
    return aesgcm.decrypt(nonce, ciphertext, None)

# Client state
username = None
sock = None
priv_key = None
pub_key_b64 = None
peers_pub = {}   # username -> public_key_bytes
pairwise_keys = {}  # username -> aes_key (derived)

def prompt_username():
    global username
    while True:
        u = input("Choose username: ").strip()
        if u and ' ' not in u and len(u) <= 32:
            username = u
            return
        print("Invalid username (no spaces, max 32 chars).")

def handle_incoming():
    global sock
    try:
        while True:
            obj = recv_json(sock)
            if obj is None:
                print("[*] Disconnected from server.")
                break
            mtype = obj.get('type')
            if mtype == 'who':
                users = obj.get('users', [])
                for u in users:
                    peers_pub[u['username']] = base64.b64decode(u['public_key'])
                    # compute pairwise key
                    pairwise_keys[u['username']] = derive_shared_key(priv_key, peers_pub[u['username']])
                print("[*] Known users:", ', '.join(peers_pub.keys()) or '(none)')
            elif mtype == 'joined':
                u = obj['username']
                pk_b64 = obj.get('public_key')
                print(f"[{obj.get('timestamp')}] >> {u} joined")
                if pk_b64:
                    peers_pub[u] = base64.b64decode(pk_b64)
                    pairwise_keys[u] = derive_shared_key(priv_key, peers_pub[u])
            elif mtype == 'left':
                u = obj['username']
                print(f"[{obj.get('timestamp')}] << {u} left")
                peers_pub.pop(u, None)
                pairwise_keys.pop(u, None)
            elif mtype == 'msg':
                # envelope: {type:'msg', from:'alice', to:'bob', cipher:..., nonce:..., timestamp:...}
                sender = obj.get('from')
                cipher_b64 = obj.get('cipher')
                nonce_b64 = obj.get('nonce')
                ts = obj.get('timestamp')
                if sender not in pairwise_keys:
                    print(f"[WARN] Received message from unknown peer {sender} — cannot decrypt.")
                    continue
                try:
                    nonce = base64.b64decode(nonce_b64)
                    cipher = base64.b64decode(cipher_b64)
                    key = pairwise_keys[sender]
                    plain = decrypt_message(key, nonce, cipher)
                    text = plain.decode('utf-8')
                    print(f"[{ts}] {sender}: {text}")
                except Exception as e:
                    print(f"[ERROR] Failed to decrypt message from {sender}: {e}")
            elif mtype == 'error':
                print("[SERVER-ERROR]", obj.get('reason'))
            else:
                print("[INFO] Unknown message from server:", obj)
    except Exception as e:
        print("[EXCEPTION in listener]", e)
    finally:
        try: sock.close()
        except: pass

def interactive_input_loop():
    global sock
    try:
        while True:
            line = input()
            if not line:
                continue
            if line.startswith('/'):
                # local commands
                if line.startswith('/quit'):
                    send_json(sock, {'type':'leave', 'username': username})
                    print("[*] Quitting.")
                    sock.close()
                    break
                elif line.startswith('/users'):
                    print("Known users:", ', '.join(peers_pub.keys()) or '(none)')
                elif line.startswith('/pm '):
                    # syntax: /pm target message...
                    parts = line.split(' ', 2)
                    if len(parts) < 3:
                        print("Usage: /pm target message")
                        continue
                    target, msg = parts[1], parts[2]
                    send_encrypted_to(target, msg)
                else:
                    print("Commands:\n  /quit\n  /users\n  /pm user message")
            else:
                # send to all known users (group): encrypt per recipient
                send_broadcast(line)
    except Exception as e:
        print("[INPUT EXCEPTION]", e)

def send_encrypted_to(target_username, text):
    if target_username not in pairwise_keys:
        print(f"[ERR] Unknown user {target_username}. Use /users to list.")
        return
    key = pairwise_keys[target_username]
    nonce, ct = encrypt_message(key, text.encode('utf-8'))
    payload = {
        'type':'msg',
        'from': username,
        'to': target_username,
        'cipher': base64.b64encode(ct).decode('utf-8'),
        'nonce': base64.b64encode(nonce).decode('utf-8'),
        'timestamp': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    }
    send_json(sock, payload)

def send_broadcast(text):
    # send one envelope per recipient (server will forward individually)
    recipients = list(pairwise_keys.keys())
    if not recipients:
        print("[WARN] No other users to send to.")
        return
    for r in recipients:
        send_encrypted_to(r, text)

def main():
    global sock, priv_key, pub_key_b64
    prompt_username()

    # generate X25519 key pair
    priv_key = x25519.X25519PrivateKey.generate()
    pub_key = priv_key.public_key().public_bytes()
    pub_key_b64 = base64.b64encode(pub_key).decode('utf-8')

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_IP, SERVER_PORT))

    # send join
    send_json(sock, {'type':'join', 'username': username, 'public_key': pub_key_b64, 'timestamp': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')})

    # start listener thread
    thr = threading.Thread(target=handle_incoming, daemon=True)
    thr.start()

    print("[*] You can now type messages. Commands: /quit, /users, /pm user message")
    interactive_input_loop()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n[QUIT]")
        try:
            send_json(sock, {'type':'leave', 'username': username})
        except:
            pass
        sys.exit(0)
