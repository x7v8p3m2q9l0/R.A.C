# aes_util.py
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64

def pad(data): return data + " " * (16 - len(data) % 16)
def unpad(data): return data.rstrip()

def encrypt(data, key):
    key = base64.b64decode(key)
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ct = cipher.encrypt(pad(data).encode())
    return base64.b64encode(iv + ct).decode()

def decrypt(data, key):
    key = base64.b64decode(key)
    raw = base64.b64decode(data)
    iv, ct = raw[:16], raw[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ct).decode())
