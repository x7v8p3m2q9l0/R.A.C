import socket, threading, json, select
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
        client_info = config["clients"].get(client_id)
        if not client_info:
            conn.send(b"INVALID CLIENT ID")
            conn.close()
            return

        clients[client_id] = {"conn": conn, "key": client_info["key"]}
        print(f"[+] Client connected: {client_id}")

        while True:
            result = conn.recv(4096)
            if not result:
                break

            for admin_id, admin in admins.items():
                try:
                    plaintext = decrypt(result.decode(), client_info["key"])
                    encrypted = encrypt(plaintext, admin["key"])
                    admin["conn"].send(json.dumps({"from": client_id, "payload": encrypted}).encode())
                except Exception as e:
                    print(f"[!] Failed to forward result to admin {admin_id}: {e}")
    except Exception as e:
        print(f"[!] Client error: {e}")
    finally:
        print(f"[-] Client disconnected: {client_id}")
        clients.pop(client_id, None)
        conn.close()

def handle_admin(conn):
    try:
        data = conn.recv(4096).decode()
        obj = json.loads(data)
        admin_id = obj["id"]
        admin_info = config["admins"].get(admin_id)
        if not admin_info:
            conn.send(b"INVALID ADMIN ID")
            conn.close()
            return

        admins[admin_id] = {"conn": conn, "key": admin_info["key"]}
        print(f"[+] Admin connected: {admin_id}")

        while True:
            payload = conn.recv(4096)
            if not payload:
                break
            obj = json.loads(payload.decode())
            cmd = decrypt(obj["payload"], admin_info["key"])

            for client_id, client in clients.items():
                try:
                    encrypted = encrypt(cmd, client["key"])
                    client["conn"].send(json.dumps({"payload": encrypted}).encode())
                except Exception as e:
                    print(f"[!] Failed to send command to {client_id}: {e}")
    except Exception as e:
        print(f"[!] Admin error: {e}")
    finally:
        print(f"[-] Admin disconnected: {admin_id}")
        admins.pop(admin_id, None)
        conn.close()

def start():
    admin_server = socket.socket()
    admin_server.bind(("0.0.0.0", 9000))
    admin_server.listen()

    client_server = socket.socket()
    client_server.bind(("0.0.0.0", 5000))
    client_server.listen()

    print("[Middleware] Listening on ports 9000 (admins) and 9001 (clients)")

    while True:
        rlist, _, _ = select.select([admin_server, client_server], [], [])
        for s in rlist:
            conn, _ = s.accept()
            if s == admin_server:
                threading.Thread(target=handle_admin, args=(conn,), daemon=True).start()
            else:
                threading.Thread(target=handle_client, args=(conn,), daemon=True).start()

if __name__ == "__main__":
    start()
