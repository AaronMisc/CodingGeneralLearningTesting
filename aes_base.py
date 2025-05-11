# pip install pycryptodome
# pip install pyperclip

"""
==About this code==
This code is a common code used for AES Encryption.
pycryptodome is used to encrypt and decrypt, containing many simple algorithms.

==About AES==
AES stands for Advanced Encryption Standard. Name: Rijndael.
It is a symmetric encryption algorithm that uses a 128/192/256-bit key.
See: https://en.wikipedia.org/wiki/Advanced_Encryption_Standard
"""

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import pyperclip

# Function to pad plaintext (AES requires padding to the block size)
def pad(text):
    padding_length = AES.block_size - len(text) % AES.block_size
    padding = chr(padding_length) * padding_length
    return text + padding

# Function to unpad plaintext after decryption
def unpad(text):
    if isinstance(text, bytes):
        text = text.decode('utf-8')  # Decode bytes to string
    padding_length = ord(text[-1])  # Get the padding length from the last character
    return text[:-padding_length]  # Remove the padding

# Encrypt function
def encrypt(plain_text, key):
    # Create random 16-byte IV
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    # Pad the plaintext and encrypt
    encrypted_text = cipher.encrypt(pad(plain_text).encode('utf-8'))
    
    # Combine IV with encrypted text and encode in base64 for easy transmission
    return base64.b64encode(iv + encrypted_text).decode('utf-8')

# Decrypt function
def decrypt(enc_text, key):
    # Decode from base64
    enc_text = base64.b64decode(enc_text)
    
    iv = enc_text[:AES.block_size]  # Extract the IV from the encrypted data
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    # Decrypt and unpad the plaintext
    decrypted_text = unpad(cipher.decrypt(enc_text[AES.block_size:]))
    
    return decrypted_text

# Function to generate a random AES key
def generate_key(number_of_bytes=16):
    return get_random_bytes(number_of_bytes)  # Generate a 16-byte key for AES-128

# Function to convert hex to bytes
def hex_to_bytes(hex_string):
    return bytes.fromhex(hex_string)    

if __name__ == "__main__":
# Example usage
    def main():
        while True:
            print("==Main Menu==")
            print("""Options:
    1. Run Program Example
    2. Generate Key
    3. Encrypt
    4. Decrypt
    q. Quit""")
            option = input("Please enter an option > ")

            if option == "1":
                key = generate_key()
                print(f"Key: \n{key.hex()}")
                plain_text = """Hello"""
                encrypted_text = encrypt(plain_text, key)
                print(f"Encrypted text: \n{encrypted_text}")
                decrypted_text = decrypt(encrypted_text, key)
                print(f"Decrypted text: \n{decrypted_text}")
            elif option == "2":
                number_of_bytes = int(input("How many bytes > "))
                key = generate_key(number_of_bytes)
                print(f"""Generated key (hex): \n{key.hex()}
    Generated key (raw): \n{key}""")
                
                copy_key_mode = input("Copy key (hex, raw)?: ")
                if copy_key_mode == "hex":
                    pyperclip.copy(key.hex())
                    print("Key hex copied.")
                elif copy_key_mode == "raw":
                    pyperclip.copy(base64.b64encode(key).decode('utf-8'))  # Copy base64 encoded key
                    print("Key copied (base64 encoded).")
            elif option == "3":
                key = input("Enter key (hex or base64) > ")
                key = base64.b64decode(key) if len(key) % 4 == 0 else hex_to_bytes(key)  # Decode the key
                plain_text = input("Enter plaintext > ")
                encrypted_text = encrypt(plain_text, key)
                print("Encrypted text: \n" + encrypted_text)
            elif option == "4":
                key = input("Enter key (hex or base64) > ")
                key = base64.b64decode(key) if len(key) % 4 == 0 else hex_to_bytes(key)  # Decode the key
                encrypted_text = input("Enter encrypted text > ")
                decrypted_text = decrypt(encrypted_text, key)
                print("Decrypted text: \n" + decrypted_text)
            elif option == "q":
                break
            else:
                print("Invalid option")

    main()
