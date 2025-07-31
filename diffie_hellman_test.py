from cryptography.hazmat.primitives.asymmetric import dh, ec
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
import base64

def to_b64(data: bytes) -> str:
    return base64.b64encode(data).decode()

def print_key_info(label, priv_key, pub_key):
    print(f"\n--- {label} ---")
    priv_bytes = priv_key.private_numbers().private_value.to_bytes(32, 'big')
    pub_bytes = pub_key.public_bytes(
        encoding=serialization.Encoding.X962,
        format=serialization.PublicFormat.UncompressedPoint
    )
    print("Private Key:", to_b64(priv_bytes))
    print("Public Key:", to_b64(pub_bytes))

def derive_session_key(private_key, peer_public_key):
    shared_key = private_key.exchange(ec.ECDH(), peer_public_key)
    derived = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'handshake data'
    ).derive(shared_key)
    return shared_key, derived

# 1. Use standard 2048-bit MODP group from RFC 3526 (Group 14)
# Generator: 2
# Prime: A known safe 2048-bit prime
p_hex = 'FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A63A3620FFFFFFFFFFFFFFFF'
p = int(p_hex, 16)
g = 2

def dhe():
    # 2. Parameter object
    dh_parameters = dh.DHParameterNumbers(p, g).parameters(default_backend())

    # 3. Each side generates private + public key pair
    client_private_key = dh_parameters.generate_private_key()
    server_private_key = dh_parameters.generate_private_key()

    client_public_key = client_private_key.public_key()
    server_public_key = server_private_key.public_key()

    # 4. Exchange public keys (simulated here on one machine)
    # Compute shared secrets
    client_shared_key = client_private_key.exchange(server_public_key)
    server_shared_key = server_private_key.exchange(client_public_key)

    # 5. Verify both sides derived the same shared secret
    assert client_shared_key == server_shared_key

    # 6. Derive a session key using HKDF
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'handshake data',
        backend=default_backend()
    ).derive(client_shared_key)

    print("== DHE Key Exchange Simulation ==")
    print("\n--- Parameters ---")
    print(f"Prime (p): {p}")
    print(f"Generator (g): {g}")

    print("\n--- Client Side ---")
    print("Private Key:", to_b64(client_private_key.private_numbers().x.to_bytes(256, 'big')))
    print("Public Key:", to_b64(client_public_key.public_numbers().y.to_bytes(256, 'big')))

    print("\n--- Server Side ---")
    print("Private Key:", to_b64(server_private_key.private_numbers().x.to_bytes(256, 'big')))
    print("Public Key:", to_b64(server_public_key.public_numbers().y.to_bytes(256, 'big')))

    print("\n--- Shared Secret ---")
    print("Client Shared Key:", to_b64(client_shared_key))
    print("Server Shared Key:", to_b64(server_shared_key))

    print("\n--- Derived Session Key (32 bytes, HKDF-SHA256) ---")
    print("Session Key:", to_b64(derived_key))


def ecdhe(multiple_clients=False):
    # PART 2
    # Curve
    curve = ec.SECP256R1()

    # Original participants
    clientA_priv = ec.generate_private_key(curve)
    server_priv = ec.generate_private_key(curve)

    clientA_pub = clientA_priv.public_key()
    server_pub = server_priv.public_key()

    if multiple_clients:
        clientB_priv = ec.generate_private_key(curve)
        clientB_pub = clientB_priv.public_key()
        sharedB_raw, sessionB = derive_session_key(clientB_priv, server_pub)
        sharedServerWithB_raw, sessionServerWithB = derive_session_key(server_priv, clientB_pub)


    # Derive shared secrets
    sharedA_raw, sessionA = derive_session_key(clientA_priv, server_pub)

    # Server also derives the same shared secret with Client A
    sharedServerWithA_raw, sessionServerWithA = derive_session_key(server_priv, clientA_pub)

    # Output
    print("== ECDHE ==")

    print_key_info("Client A", clientA_priv, clientA_pub)
    if multiple_clients: print_key_info("Client B", clientB_priv, clientB_pub)
    print_key_info("Server", server_priv, server_pub)

    print("\n--- Shared Secrets ---")
    print("Client A ⇄ Server Shared Secret:", to_b64(sharedA_raw))
    if multiple_clients: print("Client B ⇄ Server Shared Secret:", to_b64(sharedB_raw))
    print("Server ⇄ Client A Shared Secret:", to_b64(sharedServerWithA_raw))
    if multiple_clients: print("Server ⇄ Client B Shared Secret:", to_b64(sharedServerWithB_raw))

    print("\n--- Derived Session Keys (HKDF-SHA256, 32 bytes) ---")
    print("Client A ⇄ Server:", to_b64(sessionA))
    if multiple_clients: print("Client B ⇄ Server:", to_b64(sessionB))
    print("Match check (A):", sessionA == sessionServerWithA)
    if multiple_clients: print("Match check (B):", sessionB == sessionServerWithB)
    if multiple_clients: print("Mismatch check (A vs B):", sessionA != sessionB)

