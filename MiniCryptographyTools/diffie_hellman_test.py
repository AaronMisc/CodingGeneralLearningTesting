import base64
import pyperclip
from cryptography.hazmat.primitives.asymmetric import dh, ec
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

# === Utility Functions ===

def to_b64(data: bytes) -> str:
    return base64.b64encode(data).decode()

def from_b64(data: str) -> bytes:
    return base64.b64decode(data.strip())

def print_bytes(label: str, data: bytes):
    print(f"{label}: {to_b64(data)}")

def print_key_pair(label: str, private_key, public_key):
    print(f"\n--- {label} ---")
    if isinstance(private_key, ec.EllipticCurvePrivateKey):
        priv_val = private_key.private_numbers().private_value.to_bytes(32, 'big')
        pub_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.X962,
            format=serialization.PublicFormat.UncompressedPoint
        )
    elif isinstance(private_key, dh.DHPrivateKey):
        size = (private_key.key_size + 7) // 8
        priv_val = private_key.private_numbers().x.to_bytes(size, 'big')
        pub_bytes = public_key.public_numbers().y.to_bytes(size, 'big')
    else:
        raise ValueError("Unsupported key type")

    print_bytes("Private Key", priv_val)
    print_bytes("Public Key", pub_bytes)

def derive_session_key(private_key, peer_public_key):
    shared_key = private_key.exchange(ec.ECDH(), peer_public_key)
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'handshake data'
    ).derive(shared_key)
    return shared_key, derived_key

# === DHE ===

def simulate_dhe():
    print("== DHE Key Exchange Simulation ==")

    # RFC 3526 Group 14
    p_hex = (
        'FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74'
        '020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F1437'
        '4FE1356D6D51C245E485B576625E7EC6F44C42E9A63A3620FFFFFFFFFFFFFFFF'
    )
    p = int(p_hex, 16)
    g = 2
    parameters = dh.DHParameterNumbers(p, g).parameters(default_backend())

    client_priv = parameters.generate_private_key()
    server_priv = parameters.generate_private_key()

    client_pub = client_priv.public_key()
    server_pub = server_priv.public_key()

    # Exchange keys
    shared_client = client_priv.exchange(server_pub)
    shared_server = server_priv.exchange(client_pub)
    assert shared_client == shared_server

    # Derive session key
    session_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'handshake data',
        backend=default_backend()
    ).derive(shared_client)

    # Output
    print("\n--- Parameters ---")
    print(f"Prime (p): {p}")
    print(f"Generator (g): {g}")

    print_key_pair("Client", client_priv, client_pub)
    print_key_pair("Server", server_priv, server_pub)

    print("\n--- Shared Secret ---")
    print_bytes("Client Shared Key", shared_client)
    print_bytes("Server Shared Key", shared_server)

    print("\n--- Derived Session Key (HKDF-SHA256, 32 bytes) ---")
    print_bytes("Session Key", session_key)

# === ECDHE ===

def simulate_ecdhe(multiple_clients=False):
    print("== ECDHE Simulation ==")

    curve = ec.SECP256R1()

    clientA_priv = ec.generate_private_key(curve)
    server_priv = ec.generate_private_key(curve)

    clientA_pub = clientA_priv.public_key()
    server_pub = server_priv.public_key()

    sharedA_raw, sessionA = derive_session_key(clientA_priv, server_pub)
    sharedS_A_raw, sessionS_A = derive_session_key(server_priv, clientA_pub)

    print_key_pair("Client A", clientA_priv, clientA_pub)
    print_key_pair("Server", server_priv, server_pub)

    if multiple_clients:
        clientB_priv = ec.generate_private_key(curve)
        clientB_pub = clientB_priv.public_key()

        sharedB_raw, sessionB = derive_session_key(clientB_priv, server_pub)
        sharedS_B_raw, sessionS_B = derive_session_key(server_priv, clientB_pub)

        print_key_pair("Client B", clientB_priv, clientB_pub)

    print("\n--- Shared Secrets ---")
    print_bytes("Client A ⇄ Server", sharedA_raw)
    print_bytes("Server ⇄ Client A", sharedS_A_raw)
    if multiple_clients:
        print_bytes("Client B ⇄ Server", sharedB_raw)
        print_bytes("Server ⇄ Client B", sharedS_B_raw)

    print("\n--- Derived Session Keys ---")
    print_bytes("Client A ⇄ Server", sessionA)
    print(f"Match check (A): {sessionA == sessionS_A}")

    if multiple_clients:
        print_bytes("Client B ⇄ Server", sessionB)
        print(f"Match check (B): {sessionB == sessionS_B}")
        print(f"Mismatch check (A vs B): {sessionA != sessionB}")

# === ECDHE User Input ===

def ecdhe_user_input():
    print("== ECDHE: User Input Edition ==")
    curve = ec.SECP256R1()

    # Step 1: Generate client key pair
    client_priv = ec.generate_private_key(curve)
    client_pub = client_priv.public_key()

    client_pub_bytes = client_pub.public_bytes(
        encoding=serialization.Encoding.X962,
        format=serialization.PublicFormat.UncompressedPoint
    )

    # Step 2: Show public key and copy to clipboard
    client_pub_b64 = to_b64(client_pub_bytes)
    pyperclip.copy(client_pub_b64)
    print("\n[Client Public Key] (copied to clipboard):")
    print(client_pub_b64)

    # Step 3: Input server's public key (base64)
    server_pub_b64 = input("\nPaste the Server's Public Key (base64): ").strip()
    try:
        server_pub_bytes = from_b64(server_pub_b64)
        server_pub_key = ec.EllipticCurvePublicKey.from_encoded_point(curve, server_pub_bytes)
    except Exception as e:
        print(f"Error loading server public key: {e}")
        return

    # Step 4: Derive shared secret and session key
    try:
        shared_key, session_key = derive_session_key(client_priv, server_pub_key)
    except Exception as e:
        print(f"Key exchange error: {e}")
        return

    # Step 5: Output
    print("\n--- Shared Secret ---")
    print_bytes("Shared Key", shared_key)

    print("\n--- Session Key (HKDF-SHA256, 32 bytes) ---")
    print_bytes("Derived Session Key", session_key)

    print("\nSuccess. You can now send your public key to the server.")

# === Main ===

if __name__ == "__main__":
    while True:
        user_input = input("Which to run? (dhe, ecdhe, euser) > ").lower().strip()

        if user_input == "dhe":
            simulate_dhe()
        elif user_input == "ecdhe":
            simulate_ecdhe()
        elif user_input == "euser":
            ecdhe_user_input()
        else:
            break

        print("\n" * 3)