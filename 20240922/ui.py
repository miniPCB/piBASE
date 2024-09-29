from PyQt5.QtWidgets import (
    QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit
)
from data_manager import load_devices, load_users, load_checkouts

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Device Check-Out System")
        self.setGeometry(100, 100, 400, 300)
        
        self.layout = QVBoxLayout()
        
        # Load users
        self.users = load_users()
        
        # Create buttons for each user
        for user in self.users:
            button = QPushButton(user['name'], self)
            button.clicked.connect(lambda checked, user_id=user['user_id']: self.identify_user(user_id))
            self.layout.addWidget(button)

        self.barcode_input = QLineEdit(self)
        self.barcode_input.setPlaceholderText("Scan Device Barcode")
        self.barcode_input.setEnabled(False)  # Disable until user identifies themselves
        self.layout.addWidget(self.barcode_input)

        self.checkout_button = QPushButton("Check Out Device", self)
        self.checkout_button.clicked.connect(self.checkout_device)
        self.checkout_button.setEnabled(False)  # Disable until barcode is scanned
        self.layout.addWidget(self.checkout_button)

        self.result_label = QLabel("", self)
        self.layout.addWidget(self.result_label)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        self.current_user_id = None  # To track the identified user

    def identify_user(self, user_id):
        self.current_user_id = user_id
        self.result_label.setText(f"Identified User: {user_id}")
        self.barcode_input.setEnabled(True)  # Enable barcode input
        self.checkout_button.setEnabled(True)  # Enable checkout button

    def checkout_device(self):
        device_barcode = self.barcode_input.text()
        
        # Load data
        devices = load_devices()
        checkouts = load_checkouts()

        # Here you would check if the device exists using its barcode
        for device in devices:
            if device['barcode'] == device_barcode:
                # Perform checkout logic
                self.result_label.setText(f"Checked out {device['name']} to {self.current_user_id}.")
                return
        
        self.result_label.setText("Device not found.")

