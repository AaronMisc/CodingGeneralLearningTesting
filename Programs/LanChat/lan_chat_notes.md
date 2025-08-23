# Python LAN Chat with ECDH + AES-GCM

A simple **LAN chat system** written in Python, supporting:

* **Multiple clients** connected to a central server
* **Usernames**, join and leave notifications
* **Secure communication** using **ECDH (X25519)** for key exchange
* **AES-GCM** for message confidentiality & integrity
* **Per-client encryption keys** (each client has its own channel with the server)
* **Length-prefixed framing** to ensure reliable message delivery

## How It Works

### 1. Connection

* A **server** runs and waits for incoming TCP connections.
* Clients connect to the server’s LAN IP and port.

### 2. Key Exchange (ECDH Handshake)

* Server generates an **ephemeral X25519 keypair** and a random **salt**.
* Server sends its public key and the salt to the client.
* Client generates its own X25519 keypair and sends its public key back.
* Both compute the **same shared secret** using ECDH.
* A symmetric **AES-256 key** is derived from the shared secret using **HKDF-SHA256** with the provided salt.

### 3. Secure Messaging

* Every message is encrypted with **AES-GCM**:

  * A fresh **12-byte nonce** is generated for each message.
  * Message is encrypted and authenticated, producing `(nonce | tag | ciphertext)`.
* Messages are sent as **length-prefixed packets**:

  ```
  [4-byte length][encrypted message]
  ```

  This avoids TCP message boundary issues.

### 4. Chat Features

* Clients choose a **username** (encrypted during exchange).
* Server broadcasts **join/leave events**.
* Messages are decrypted and displayed with usernames.
* Each client has a unique **AES key** with the server.

## Requirements

* Python **3.8+**
* Dependencies:

  ```bash
  pip install cryptography
  ```

## Usage

### 1. Start the Server

Run on the machine that will host the chat:

```bash
python server_ecdh_chat.py
```

Output:

```
💻 Server listening on 0.0.0.0:5000
```

The server listens for connections on **port 5000** by default.

### 2. Find Server’s LAN IP

On the server machine, get its LAN IP:

* Windows:

  ```bash
  ipconfig
  ```
* Linux / Mac:

  ```bash
  ifconfig
  ```

Look for something like `192.168.x.x`.

### 3. Connect Clients

On each client machine:

```bash
python client_ecdh_chat.py
```

Edit the bottom of the client script to replace:

```python
client("192.168.1.100")
```

with your server’s LAN IP.

### 4. Start Chatting

* Each client will be prompted for a **username**.
* Messages are **encrypted** and sent via the server.
* Join/leave events are broadcast to all users.

## Security Model

* **ECDH (X25519):** Provides secure key exchange over an insecure LAN.
* **AES-GCM:** Provides confidentiality, integrity, and authenticity of messages.
* **Per-client keys:** Each client has a unique key with the server.
* **Limitation:** Currently, the server’s ECDH key is not authenticated → possible **man-in-the-middle (MITM)** if someone controls the LAN.

# Lan Chat Mini
A smaller simpler lan chat.
Doesn't include end-to-end encryption.