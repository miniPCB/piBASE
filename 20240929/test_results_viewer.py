import sys
import os
import json
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QTabWidget, QLabel, QPushButton,
                             QListWidget, QHBoxLayout, QFileDialog, QTextEdit)
from PyQt5.QtCore import Qt

class TestApplication(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Tester Application")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        # Tab widget to hold different pages
        self.tabs = QTabWidget()
        self.test_info_tab = QWidget()
        self.tests_ran_tab = QWidget()
        self.test_results_tab = QWidget()

        # Adding tabs
        self.tabs.addTab(self.test_info_tab, "Test Information")
        self.tabs.addTab(self.tests_ran_tab, "Tests Ran")
        self.tabs.addTab(self.test_results_tab, "Test Results")

        # Layout for each tab
        self.setupTestInfoTab()
        self.setupTestsRanTab()
        self.setupTestResultsTab()

        layout.addWidget(self.tabs)
        self.setLayout(layout)

        self.data_folder = os.path.join(os.getcwd(), 'data')
        self.all_test_data = []

        # Load all JSON files from the /data/ folder on startup
        self.loadAllTestFiles()

    def setupTestInfoTab(self):
        layout = QVBoxLayout()

        self.test_selector = QLabel("Select Test to Run:")
        layout.addWidget(self.test_selector)

        # Button to load additional tests manually
        self.load_tests_button = QPushButton("Load Additional Tests")
        self.load_tests_button.clicked.connect(self.loadTestsManually)
        layout.addWidget(self.load_tests_button)

        self.test_info_tab.setLayout(layout)

    def setupTestsRanTab(self):
        layout = QVBoxLayout()

        self.tests_ran_list = QListWidget()
        self.tests_ran_list.itemDoubleClicked.connect(self.openTestResult)
        layout.addWidget(self.tests_ran_list)

        self.tests_ran_tab.setLayout(layout)

    def setupTestResultsTab(self):
        layout = QVBoxLayout()

        self.test_results_display = QTextEdit()
        self.test_results_display.setReadOnly(True)
        layout.addWidget(self.test_results_display)

        self.test_results_tab.setLayout(layout)

    def loadTestsManually(self):
        # Let user choose a JSON file from the /data/ directory
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Open Test Data", self.data_folder, "JSON Files (*.json)")

        if file_path:
            self.loadTestData(file_path)

    def loadAllTestFiles(self):
        """Loads all JSON test files from the data folder on startup."""
        if os.path.exists(self.data_folder):
            for file_name in os.listdir(self.data_folder):
                if file_name.endswith('.json'):
                    file_path = os.path.join(self.data_folder, file_name)
                    self.loadTestData(file_path)

    def loadTestData(self, file_path):
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)

            # Store the loaded test data
            self.all_test_data.append(data)

            # Add test events to the list
            for test_event in data.get('test_events', []):
                test_date = test_event.get('date_time', 'Unknown Date')
                device_id = data.get('device_id', 'Unknown Device')
                list_item_text = f"{device_id} - Test Ran on {test_date}"
                self.tests_ran_list.addItem(list_item_text)

        except Exception as e:
            self.test_selector.setText(f"Error loading tests: {str(e)}")

    def openTestResult(self, item):
        selected_test_index = self.tests_ran_list.row(item)

        if selected_test_index >= 0:
            # Find the corresponding test event based on the selected index
            test_event = None
            current_index = 0
            for data in self.all_test_data:
                for event in data['test_events']:
                    if current_index == selected_test_index:
                        test_event = event
                        break
                    current_index += 1
                if test_event:
                    break

            # Display the test details
            if test_event:
                self.showTestResults(test_event)

    def showTestResults(self, test_event):
        # Create an HTML formatted string with a table that resizes to 100% of the window width
        test_results_html = f"""
        <html>
        <body>
        <h2>Test Ran on: {test_event['date_time']}</h2>
        <p><b>Tester:</b> {test_event['user_id']} (ID: {test_event['tester_id']})</p>
        <p><b>Tester Calibration Due:</b> {test_event['date_tester_calibration_due']}</p>
        <h3>Test Results:</h3>
        <table border="1" cellpadding="5" cellspacing="0" style="width:100%;">
            <tr>
                <th>Test #</th>
                <th>Test Name</th>
                <th>Target Value</th>
                <th>Measured Value</th>
                <th>Conclusion</th>
            </tr>
        """

        for result in test_event.get('test_results', []):
            # Determine the unit based on measurement type
            unit = 'A' if result['measurement_type'] == 'Current' else 'V'
            
            # Conditional formatting for Pass/Fail
            if result['conclusion'] == 'Pass':
                conclusion_color = 'background-color: green; color: white;'
            else:
                conclusion_color = 'background-color: red; color: white;'

            test_results_html += f"""
            <tr>
                <td>{result['test_number']}</td>
                <td>{result['test_name']}</td>
                <td>{result['target_value']} {unit}</td>
                <td>{result['measured_value']} {unit}</td>
                <td style="{conclusion_color}"><b>{result['conclusion']}</b></td>
            </tr>
            """

        test_results_html += """
        </table>
        </body>
        </html>
        """

        # Switch to the Test Results tab and display the formatted HTML
        self.tabs.setCurrentIndex(2)
        self.test_results_display.setHtml(test_results_html)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TestApplication()
    ex.show()
    sys.exit(app.exec_())
