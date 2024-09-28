import sys
import os
import json
import subprocess
import pkg_resources
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QScrollArea, QGridLayout, QLabel, QTabWidget, QTextEdit
)
from PyQt5.QtCore import Qt, QEvent

# Function to install or upgrade pip to the latest version
def upgrade_pip():
    try:
        # Use the path to the Python executable in the user's environment
        python_executable = sys.executable
        # Run the command to upgrade pip
        subprocess.check_call([python_executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
        print("Pip upgraded to the latest version.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to upgrade pip: {e}")

# Function to install a package using pip
def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Function to check if PyQt5 is installed and install it if not
def ensure_pyqt_installed():
    try:
        pkg_resources.get_distribution('PyQt5')
    except pkg_resources.DistributionNotFound:
        print("PyQt5 not found. Installing...")
        install_package('PyQt5')

# Ensure PyQt5 is installed
ensure_pyqt_installed()

# Upgrade pip to the latest version
upgrade_pip()

class JSONViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        # Main layout of the window
        main_layout = QVBoxLayout()

        # Tab widget to hold the tabs
        self.tab_widget = QTabWidget(self)

        # Add a main tab for displaying the list of data files (formerly "JSON Files")
        self.main_tab = QWidget()
        self.main_layout = QVBoxLayout(self.main_tab)

        # Scroll area for dynamic content display
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        
        # Create a widget that will contain the rows
        container_widget = QWidget()
        self.grid_layout = QGridLayout(container_widget)
        
        # Populate the grid with rows of data file content
        self.populate_grid()

        # Set the container widget as the scroll area's widget
        scroll_area.setWidget(container_widget)
        
        # Add scroll area to the main layout of the main tab
        self.main_layout.addWidget(scroll_area)

        # Add the main tab to the tab widget
        self.tab_widget.addTab(self.main_tab, "Data Files")

        # Add a single data tab for displaying JSON content
        self.data_tab = QWidget()
        self.data_layout = QVBoxLayout(self.data_tab)

        # Add a text edit widget to display the JSON content as HTML
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.data_layout.addWidget(self.text_edit)

        # Add the data tab to the tab widget
        self.tab_widget.addTab(self.data_tab, "Data View")

        # Add the tab widget to the main window's layout
        main_layout.addWidget(self.tab_widget)

        # Set the layout for the main widget
        self.setLayout(main_layout)

        # Window settings (1280x850)
        self.setWindowTitle("JSON File Viewer")
        self.setGeometry(100, 100, 1280, 850)

    def populate_grid(self):
        # Get the path to the data folder
        data_folder = os.path.join(os.getcwd(), 'data')

        # Check if data folder exists
        if not os.path.exists(data_folder):
            os.makedirs(data_folder)  # Create the folder if it doesn't exist
            return
        
        # List all JSON files in the /data/ folder
        json_files = [f for f in os.listdir(data_folder) if f.endswith('.json')]

        if not json_files:
            return

        # Define the max height for each row (0.5 inches -> ~48 pixels)
        row_height = 48

        # Iterate over each JSON file and display rows
        for idx, json_file in enumerate(json_files):
            try:
                file_path = os.path.join(data_folder, json_file)

                # Open and read the JSON file
                with open(file_path, 'r') as file:
                    data = json.load(file)

                # Extract relevant information (e.g., device_id, board_name, variant)
                device_id = data.get("device_id", "Unknown")
                board_name = data.get("device_information", {}).get("board_name", "Unknown")
                variant = data.get("device_information", {}).get("variant", "Unknown")
                
                # Create labels to display the extracted information
                device_label = QLabel(f"Device ID: {device_id}", self)
                board_label = QLabel(f"Board Name: {board_name}", self)
                variant_label = QLabel(f"Variant: {variant}", self)

                # Set fixed height for each label (max height 48 pixels, approx. 0.5 inches)
                device_label.setFixedHeight(row_height)
                board_label.setFixedHeight(row_height)
                variant_label.setFixedHeight(row_height)

                # Add hover effect using event filters
                self.install_hover_effect(device_label)
                self.install_hover_effect(board_label)
                self.install_hover_effect(variant_label)

                # Add labels to grid layout (one row per JSON file)
                self.grid_layout.addWidget(device_label, idx, 0)
                self.grid_layout.addWidget(board_label, idx, 1)
                self.grid_layout.addWidget(variant_label, idx, 2)

                # Handle double-click events on labels
                device_label.mouseDoubleClickEvent = lambda event, f=file_path: self.refresh_data_tab(f)
                board_label.mouseDoubleClickEvent = lambda event, f=file_path: self.refresh_data_tab(f)
                variant_label.mouseDoubleClickEvent = lambda event, f=file_path: self.refresh_data_tab(f)

            except Exception as e:
                error_label = QLabel(f"Error loading {json_file}: {e}", self)
                error_label.setFixedHeight(row_height)
                self.grid_layout.addWidget(error_label, idx, 0)

    def install_hover_effect(self, widget):
        # Install an event filter on the widget to track hover events
        widget.installEventFilter(self)

    def eventFilter(self, source, event):
        # Handle hover events to change background color on hover
        if event.type() == QEvent.Enter:
            source.setStyleSheet("background-color: lightblue;")
        elif event.type() == QEvent.Leave:
            source.setStyleSheet("")
        return super(JSONViewer, self).eventFilter(source, event)

    def refresh_data_tab(self, file_path):
        # Read the JSON data from the file
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)

            # Convert JSON data to HTML format
            html_content = self.json_to_html(data)

            # Set the HTML content of the text edit widget
            self.text_edit.setHtml(html_content)

            # Switch to the data tab
            self.tab_widget.setCurrentWidget(self.data_tab)

        except Exception as e:
            self.text_edit.setText(f"Error reading file: {file_path} - {e}")

    def json_to_html(self, data):
        # Helper function to generate HTML table for process and red tag labels
        def generate_label_table(labels, label_type):
            if not labels:
                return f"<b>{label_type}:</b> No data<br>"

            html = f"<b>{label_type}:</b><br><table border='1' style='border-collapse: collapse; width: 100%;'>"
            html += "<tr><th>Label</th><th>Date Applied</th><th>Computer ID</th><th>User ID</th></tr>"
            for label in labels:
                html += f"<tr><td>{label.get('label', 'N/A')}</td><td>{label.get('date_applied', 'N/A')}</td>"
                html += f"<td>{label.get('computer_id', 'N/A')}</td><td>{label.get('user_id', 'N/A')}</td></tr>"
            html += "</table><br>"
            return html

        # Helper function to generate HTML table for test events
        def generate_test_events_table(test_events):
            if not test_events:
                return "<b>Test Events:</b> No data<br>"

            html = ""
            for event in test_events:
                html += f"<b>Test Event:</b> {event.get('date_time', 'N/A')}<br>"
                html += f"<b>Computer ID:</b> {event.get('computer_id', 'N/A')}<br>"
                html += f"<b>User ID:</b> {event.get('user_id', 'N/A')}<br>"
                html += f"<b>Tester ID:</b> {event.get('tester_id', 'N/A')}<br>"
                html += f"<b>Calibration Due:</b> {event.get('date_tester_calibration_due', 'N/A')}<br>"

                # Test results table
                test_results = event.get('test_results', [])
                html += generate_test_results_table(test_results)

            return html

        # Helper function to generate HTML table for test results
        def generate_test_results_table(test_results):
            if not test_results:
                return "<b>Test Results:</b> No data<br>"

            html = "<b>Test Results:</b><br><table border='1' style='border-collapse: collapse; width: 100%;'>"
            html += "<tr><th>Test #</th><th>Name</th><th>Description</th><th>Measurement Type</th><th>Target</th>"
            html += "<th>Lower Limit</th><th>Upper Limit</th><th>Measured</th><th>Conclusion</th></tr>"
            for result in test_results:
                html += f"<tr><td>{result.get('test_number', 'N/A')}</td>"
                html += f"<td>{result.get('test_name', 'N/A')}</td>"
                html += f"<td>{result.get('test_description', 'N/A')}</td>"
                html += f"<td>{result.get('measurement_type', 'N/A')}</td>"
                html += f"<td>{result.get('target_value', 'N/A')}</td>"
                html += f"<td>{result.get('lower_limit', 'N/A')}</td>"
                html += f"<td>{result.get('upper_limit', 'N/A')}</td>"
                html += f"<td>{result.get('measured_value', 'N/A')}</td>"
                html += f"<td>{result.get('conclusion', 'N/A')}</td></tr>"
            html += "</table><br>"
            return html

        # Convert a JSON object to an HTML table
        def recursive_json_to_html(json_data):
            html = "<table border='1' style='border-collapse: collapse; width: 100%;'>"
            for key, value in json_data.items():
                if isinstance(value, dict):
                    html += f"<tr><td><b>{key}</b></td><td>{recursive_json_to_html(value)}</td></tr>"
                elif isinstance(value, list):
                    if key in ["process_labels", "red_tag_labels"]:
                        # Format process labels and red tag labels into HTML tables
                        html += f"<tr><td colspan='2'>{generate_label_table(value, key)}</td></tr>"
                    elif key == "test_events":
                        # Format test events into an HTML table
                        html += f"<tr><td colspan='2'>{generate_test_events_table(value)}</td></tr>"
                else:
                    html += f"<tr><td><b>{key}</b></td><td>{value}</td></tr>"
            html += "</table>"
            return html

        # Start HTML document with CSS for responsive font size and width
        html_content = """
        <html>
        <head>
            <style>
                table { width: 100%; }
                th, td { padding: 8px; text-align: left; }
                body { font-size: 1.2vw; }  /* Responsive font size based on viewport width */
            </style>
        </head>
        <body>
        """
        html_content += recursive_json_to_html(data)
        html_content += "</body></html>"

        return html_content


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = JSONViewer()
    viewer.show()
    sys.exit(app.exec_())
