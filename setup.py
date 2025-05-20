# setup_utils.py
import uuid
import base64
import os
import json

CONFIG_FILE = "identity_config.json"

def generate_aes_key():
    return base64.b64encode(os.urandom(32)).decode()

def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {"admins": {}, "clients": {}}
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

def create_user():
    user_type = input("Create (a)dmin or (c)lient? ").lower()
    if user_type not in ("a", "c"):
        print("Invalid type.")
        return

    name = input("Enter display name (optional): ")
    user_id = str(uuid.uuid4())
    aes_key = generate_aes_key()

    config = load_config()

    if user_type == "a":
        role = input("Admin role? (admin / superadmin): ").strip().lower()
        if role not in ("admin", "superadmin"):
            print("Invalid role.")
            return
        config["admins"][user_id] = {
            "name": name,
            "role": role,
            "key": aes_key
        }
    else:
        config["clients"][user_id] = {
            "name": name,
            "key": aes_key
        }

    save_config(config)
    print(f"\n✅ Created {'Admin' if user_type == 'a' else 'Client'}:")
    print(f"  UUID: {user_id}")
    print(f"  Key: {aes_key}")
    print("  (Saved to identity_config.json)")

if __name__ == "__main__":
    create_user()
