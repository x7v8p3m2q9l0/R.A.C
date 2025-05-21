import socket, json
from aes_util import encrypt, decrypt

ADMIN_ID = "bb08b762-9015-4974-a4dd-96581e4dcefa"
SHARED_KEY = "lPiFNu8lUEVxqEKE7RM1W/r957VjxGYRMcWXYuDc42c="

s = socket.socket()
s.connect(("127.0.0.1", 9000))
s.send(json.dumps({"id": ADMIN_ID}).encode())

while True:
    cmd = input("Command to send: ").strip()
    if not cmd: continue
    encrypted = encrypt(cmd, SHARED_KEY)
    s.send(json.dumps({"id": ADMIN_ID, "payload": encrypted}).encode())

    try:
        result = json.loads(s.recv(4096).decode())
        output = decrypt(result["payload"], SHARED_KEY)
        print(f"[{result['from']}] → {output}")
    except Exception as e:
        print(f"[!] Failed to read response: {e}")
