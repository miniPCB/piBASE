import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout, QSlider, QLCDNumber)
from PyQt5.QtCore import Qt, QTimer
import random

class FanControl(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize UI components
        self.init_ui()

        # Timer for updating motor parameters
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_motor_parameters)
        self.timer.start(1000)  # Update every second

        # Motor parameters (simulated)
        self.pwm = 50  # Initial PWM setting (percentage)
        self.rpm = 0
        self.voltage = 12.0
        self.current = 0.0
        self.power = 0.0

    def init_ui(self):
        # Set up the main layout
        layout = QVBoxLayout()

        # PWM Setting Slider
        self.pwm_slider = QSlider(Qt.Horizontal)
        self.pwm_slider.setMinimum(0)
        self.pwm_slider.setMaximum(100)
        self.pwm_slider.setValue(50)
        self.pwm_slider.valueChanged.connect(self.update_pwm)
        layout.addWidget(QLabel('PWM Setting (%)'))
        layout.addWidget(self.pwm_slider)

        # Fan RPM Display
        self.rpm_display = QLCDNumber()
        layout.addWidget(QLabel('Fan RPM'))
        layout.addWidget(self.rpm_display)

        # Motor Voltage Display
        self.voltage_display = QLCDNumber()
        layout.addWidget(QLabel('Motor Voltage (V)'))
        layout.addWidget(self.voltage_display)

        # Motor Current Display
        self.current_display = QLCDNumber()
        layout.addWidget(QLabel('Motor Current (A)'))
        layout.addWidget(self.current_display)

        # Motor Power Display
        self.power_display = QLCDNumber()
        layout.addWidget(QLabel('Motor Power (W)'))
        layout.addWidget(self.power_display)

        # Set the layout to the window
        self.setLayout(layout)

        # Set window title and size
        self.setWindowTitle('Fan Motor Control')
        self.setGeometry(100, 100, 300, 400)

    def update_pwm(self):
        """Updates the PWM setting when the slider is changed."""
        self.pwm = self.pwm_slider.value()

    def update_motor_parameters(self):
        """Simulates motor parameters and updates the display."""
        # Simulate motor RPM based on PWM
        self.rpm = int(self.pwm * 20)

        # Simulate voltage (fixed in this example)
        self.voltage = 380

        # Simulate current (proportional to PWM)
        self.current = self.pwm * random.uniform(0.03, 0.04)

        # Simulate power (voltage * current)
        self.power = round(self.voltage * self.current, 2)

        # Update the displays
        self.rpm_display.display(self.rpm)
        self.voltage_display.display(self.voltage)
        self.current_display.display(round(self.current, 2))
        self.power_display.display(self.power)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FanControl()
    window.show()
    sys.exit(app.exec_())
