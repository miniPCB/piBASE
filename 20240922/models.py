class Device:
    def __init__(self, device_id, name, device_type, barcode):
        self.device_id = device_id
        self.name = name
        self.device_type = device_type
        self.barcode = barcode

class User:
    def __init__(self, user_id, name, contact):
        self.user_id = user_id
        self.name = name
        self.contact = contact

class Checkout:
    def __init__(self, device_id, user_id, checkout_date, checkin_date=None, condition='good'):
        self.device_id = device_id
        self.user_id = user_id
        self.checkout_date = checkout_date
        self.checkin_date = checkin_date
        self.condition = condition
