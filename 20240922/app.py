import sys
import subprocess

# Function to install PyQt5
def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Check for PyQt5 installation
try:
    from PyQt5.QtWidgets import QApplication, QMainWindow
except ImportError:
    print("PyQt5 is not installed. Installing now...")
    install_package("PyQt5")
    from PyQt5.QtWidgets import QApplication, QMainWindow  # Try importing again

from ui import MainWindow

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
