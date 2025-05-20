# admin_client.py
import socket, json
from aes_util import encrypt
ADMIN_ID = "bb08b762-9015-4974-a4dd-96581e4dcefa"
SHARED_KEY = "lPiFNu8lUEVxqEKE7RM1W/r957VjxGYRMcWXYuDc42c="

s = socket.socket()
s.connect(("127.0.0.1", 9000))

while True:
    cmd = input("Command to send: ")
    encrypted = encrypt(cmd, SHARED_KEY)
    s.send(json.dumps({"id": ADMIN_ID, "payload": encrypted}).encode())
    print(s.recv(4096).decode())
