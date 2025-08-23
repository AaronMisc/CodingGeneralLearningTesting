Features: 

    a server (simple relay) and a client (CLI) that together provide:

    usernames (chosen at client start; server enforces uniqueness)

    join / leave announcements (broadcast to all) with timestamps

    message timestamps (ISO 8601)

    end-to-end encryption using X25519 Diffie–Hellman (clients perform key agreement) + AES-GCM for symmetric encryption — the server only relays ciphertexts and cannot decrypt messages.

Design notes (short):

    The server is intentionally simple and does not know or use private keys — it only relays JSON messages between clients. It also broadcasts join/leave notifications.

    The clients generate X25519 keypairs on startup and publish their public key to the server. Each client keeps a mapping username → public key and derives pairwise symmetric keys with HKDF when needed. For group messages the client encrypts separate ciphertexts per recipient and sends one envelope per recipient to the server.

    All TCP messages are length-prefixed (4 byte big-endian) JSON objects so framing is robust.

    Uses cryptography library (x25519, HKDF, AESGCM). Install via pip install cryptography.

How to use

    Start the server on a machine reachable on the LAN:

python lan_chat_server.py

Make sure the server host machine firewall allows the port (default 5001).

On each client machine, edit lan_chat_client.py to set SERVER_IP to the server's LAN IP, then run:

    python lan_chat_client.py

    Choose a username when prompted. The client will generate keys automatically and announce itself.

    Commands in client:

        Type plain text and press Enter → message will be encrypted per recipient and sent to all known users.

        /pm username message → send encrypted private message to a single user

        /users → list known peers

        /quit → leave

    Message timestamps are attached by the sender as ISO 8601 UTC.

Security notes & caveats

    End-to-end: This approach produces E2E encryption between clients because each message is encrypted with a symmetric key derived from a direct X25519 exchange between the sender and that recipient. The server only sees ciphertexts and public keys.

    Perfect forward secrecy: Using ephemeral X25519 keypairs per client instance gives some forward secrecy between sessions; however if a client stores its private key between runs you get persistence. For true ephemeral PFS you could rotate keys or derive ephemeral keys for each message run.

    Authentication: This demo does not authenticate keys to usernames (i.e., a malicious actor could claim another username and pubkey). For a stronger design, you would add an authenticity layer (e.g., signatures, trust-on-first-use prompts, or a PKI).

    Group messages: Group messages are implemented by encrypting a separate ciphertext per recipient. This is simple and secure but increases bandwidth proportionally to recipients. For very large groups consider a group key management scheme (e.g. MLS) — out of scope here.

    Replay protections: AES-GCM with random nonces is used; nonces are random 96-bit values. For robust replay protection you could include message counters and maintain per-peer message sequence validation (not implemented).

    Server trust: Server trusts the initial join username claim. The server enforces username uniqueness but does not verify identity — if stronger server-side authentication is required, integrate authentication (passwords, TLS, or certificates).

    TLS: TCP streams here are plaintext. Although message contents are encrypted E2E, metadata (IP addresses, message sizes, join/leave events) are visible to the server and network. If you want to hide metadata from the server, you'd need a different architecture (peer-to-peer or onion routing).