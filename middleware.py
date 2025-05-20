import socket, threading, json
import select
from aes_util import encrypt, decrypt
from setup import load_config

clients = {}   # client_id: conn
admins = {}    # admin_id: conn
config = load_config()

def handle_client(conn):
    try:
        data = conn.recv(4096).decode()
        obj = json.loads(data)
        client_id = obj["id"]
        clients[client_id] = conn

        client_info = config["clients"].get(client_id)
        if not client_info:
            conn.send(b"INVALID CLIENT ID")
            return

        while True:
            result = conn.recv(4096).decode()
            print(f"[{client_id}] Received encrypted result")

            # Find the admin to send it back to
            for admin_id, admin_conn in admins.items():
                admin_info = config["admins"].get(admin_id)
                if admin_info:
                    decrypted_output = decrypt(result, client_info["key"])
                    encrypted_for_admin = encrypt(decrypted_output, admin_info["key"])
                    admin_conn.send(json.dumps({"from": client_id, "payload": encrypted_for_admin}).encode())
    except:
        print(f"[{client_id}] disconnected")
        clients.pop(client_id, None)

def handle_admin(conn):
    try:
        data = conn.recv(4096).decode()
        obj = json.loads(data)
        admin_id = obj["id"]
        admins[admin_id] = conn

        admin_info = config["admins"].get(admin_id)
        if not admin_info:
            conn.send(b"INVALID ADMIN ID")
            return

        while True:
            obj = json.loads(conn.recv(4096).decode())
            client_cmd = decrypt(obj["payload"], admin_info["key"])
            print(f"[{admin_id}] Sent command: {client_cmd}")

            # Forward to all clients
            for client_id, client_conn in clients.items():
                client_info = config["clients"].get(client_id)
                if client_info:
                    encrypted_for_client = encrypt(client_cmd, client_info["key"])
                    client_conn.send(json.dumps({"payload": encrypted_for_client}).encode())
    except:
        print(f"[{admin_id}] disconnected")
        admins.pop(admin_id, None)

def start():
    admin_server = socket.socket()
    admin_server.bind(("0.0.0.0", 9000))
    admin_server.listen()

    client_server = socket.socket()
    client_server.bind(("0.0.0.0", 9001))
    client_server.listen()

    print("[Middleware] Listening on ports 9000 (admin) and 9001 (clients)")

    while True:
        r1, _, _ = select.select([admin_server, client_server], [], [])
        for s in r1:
            conn, _ = s.accept()
            if s == admin_server:
                threading.Thread(target=handle_admin, args=(conn,), daemon=True).start()
            else:
                threading.Thread(target=handle_client, args=(conn,), daemon=True).start()

if __name__ == "__main__":
    start()
