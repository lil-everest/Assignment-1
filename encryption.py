from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import os

key = os.getenv("NOT_MY_KEY").encode()

def encrypt_data(data: str):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data.encode()) + padder.finalize()
    encrypted = encryptor.update(padded_data) + encryptor.finalize()
    return iv.hex(), encrypted.hex()

def decrypt_data(iv_hex: str, encrypted_hex: str):
    iv = bytes.fromhex(iv_hex)
    encrypted = bytes.fromhex(encrypted_hex)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    decrypted = decryptor.update(encrypted) + decryptor.finalize()
    return decrypted.decode().strip()
