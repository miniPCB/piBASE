import json
from config import DEVICES_FILE, USERS_FILE, CHECKOUTS_FILE

def load_devices():
    with open(DEVICES_FILE, 'r') as file:
        return json.load(file)

def load_users():
    with open(USERS_FILE, 'r') as file:
        return json.load(file)

def load_checkouts():
    with open(CHECKOUTS_FILE, 'r') as file:
        return json.load(file)

def save_devices(devices):
    with open(DEVICES_FILE, 'w') as file:
        json.dump(devices, file, indent=4)

def save_users(users):
    with open(USERS_FILE, 'w') as file:
        json.dump(users, file, indent=4)

def save_checkouts(checkouts):
    with open(CHECKOUTS_FILE, 'w') as file:
        json.dump(checkouts, file, indent=4)

def add_device(devices, new_device):
    devices.append(new_device)
    save_devices(devices)

def checkout_device(checkouts, device_id, user_id):
    checkout_entry = {
        "device_id": device_id,
        "user_id": user_id,
        "checkout_date": "current_date",
        "checkin_date": None,
        "condition": "good"
    }
    checkouts.append(checkout_entry)
    save_checkouts(checkouts)
