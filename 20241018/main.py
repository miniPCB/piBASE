import sys
import os
import subprocess
import pkg_resources

# List of required packages
required = {'PyQt5', 'PyMuPDF'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed

# Install missing packages
if missing:
    print(f"Installing missing packages: {', '.join(missing)}")
    python = sys.executable
    subprocess.check_call([python, '-m', 'pip', 'install', *missing])

# Import libraries after ensuring they are installed
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QFileDialog, QVBoxLayout, QWidget, QSplitter, QListWidget, QListWidgetItem, QLabel, QScrollArea, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtCore import Qt
import fitz  # PyMuPDF for handling PDF files

class ClickableBox(QLabel):
    """A transparent box for navigation with text."""
    def __init__(self, pdf_viewer, position='left', text='Previous Page'):
        super().__init__(text)
        self.pdf_viewer = pdf_viewer
        self.position = position
        self.setMouseTracking(True)  # Enable hover tracking
        self.setAlignment(Qt.AlignCenter)

        # Styling for the navigation box
        self.setStyleSheet("""
            background-color: rgba(0, 0, 0, 50);  /* Light transparent background */
            color: white;
            font-size: 14px;
            border-radius: 10px;  /* Rounded corners */
            border: 2px solid rgba(255, 255, 255, 50);  /* Transparent border */
        """)

    def enterEvent(self, event):
        """Change appearance on hover."""
        self.setStyleSheet("""
            background-color: rgba(100, 100, 100, 150);  /* Darker on hover */
            color: white;
            font-size: 14px;
            border-radius: 10px;
            border: 2px solid rgba(255, 255, 255, 50);
        """)

    def leaveEvent(self, event):
        """Revert to original appearance when not hovered."""
        self.setStyleSheet("""
            background-color: rgba(0, 0, 0, 50);
            color: white;
            font-size: 14px;
            border-radius: 10px;
            border: 2px solid rgba(255, 255, 255, 50);
        """)

    def mousePressEvent(self, event):
        """Handle click event to navigate pages."""
        if self.position == 'left':
            self.pdf_viewer.prev_page()
        elif self.position == 'right':
            self.pdf_viewer.next_page()


class PDFViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('PDF Viewer')
        self.setGeometry(200, 100, 800, 600)

        # Main layout with splitter
        self.splitter = QSplitter(Qt.Horizontal, self)
        self.setCentralWidget(self.splitter)

        # Initialize the left pane for listing PDF files
        self.file_list = QListWidget()
        self.file_list.setFixedWidth(250)
        self.splitter.addWidget(self.file_list)
        
        # Initialize central widget and layout for PDF display
        self.central_widget = QWidget()
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        self.splitter.addWidget(self.central_widget)
        
        # Create a label to display PDF page
        self.pdf_label = QLabel()
        self.pdf_label.setAlignment(Qt.AlignCenter)

        # Set up scroll area to allow scrolling and center-align the PDF
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.pdf_label)
        self.scroll_area.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)  # Center align PDF
        self.layout.addWidget(self.scroll_area)

        # Create "Previous Page" and "Next Page" navigation boxes
        self.prev_box = ClickableBox(self, position='left', text='Previous Page')
        self.next_box = ClickableBox(self, position='right', text='Next Page')

        # Add navigation boxes to the layout
        self.prev_box.setParent(self)
        self.next_box.setParent(self)

        # Set up positioning of the boxes slightly into the viewable area (25px)
        self.prev_box.setGeometry(285, self.height() // 2 - 25, 120, 50)  # Left box (120x50px), 25px into viewable area
        self.next_box.setGeometry(self.width() - 155, self.height() // 2 - 25, 120, 50)  # Right box (120x50px), 25px into viewable area

        # Adjust positions on window resize
        self.resizeEvent = self.adjust_navigation_boxes

        # Current PDF document, page number, and total pages
        self.pdf_document = None
        self.current_page = 0
        self.total_pages = 0

        # Zoom factor
        self.zoom_factor = 1.0

        # Dark Mode / Light Mode toggle state
        self.dark_mode = False

        # Create menu bar
        self.create_menu()

        # Populate the PDF list from the records directory
        self.load_pdf_list()

        # Connect file selection to PDF loading
        self.file_list.itemClicked.connect(self.load_selected_pdf)
        
    def create_menu(self):
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu('File')

        open_action = QAction('Open', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        close_action = QAction('Close', self)
        close_action.setShortcut('Ctrl+W')
        close_action.triggered.connect(self.close_file)
        file_menu.addAction(close_action)

        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # View menu
        view_menu = menubar.addMenu('View')

        zoom_in_action = QAction('Zoom In', self)
        zoom_in_action.setShortcut('Ctrl++')
        zoom_in_action.triggered.connect(self.zoom_in)
        view_menu.addAction(zoom_in_action)

        zoom_out_action = QAction('Zoom Out', self)
        zoom_out_action.setShortcut('Ctrl+-')
        zoom_out_action.triggered.connect(self.zoom_out)
        view_menu.addAction(zoom_out_action)

        fit_to_width_action = QAction('Fit to Width', self)
        fit_to_width_action.setShortcut('Ctrl+F')
        fit_to_width_action.triggered.connect(self.fit_to_width)
        view_menu.addAction(fit_to_width_action)

        # Navigation menu
        nav_menu = menubar.addMenu('Navigate')

        prev_page_action = QAction('Previous Page', self)
        prev_page_action.setShortcut('Ctrl+Left')
        prev_page_action.triggered.connect(self.prev_page)
        nav_menu.addAction(prev_page_action)

        next_page_action = QAction('Next Page', self)
        next_page_action.setShortcut('Ctrl+Right')
        next_page_action.triggered.connect(self.next_page)
        nav_menu.addAction(next_page_action)

        # Settings menu
        settings_menu = menubar.addMenu('Settings')

        self.dark_mode_action = QAction('Dark Mode', self)
        self.dark_mode_action.triggered.connect(self.toggle_dark_mode)
        settings_menu.addAction(self.dark_mode_action)

    def load_pdf_list(self):
        """Loads all PDF files from the 'records' directory into the list pane."""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        records_dir = os.path.join(script_dir, 'records')

        if not os.path.exists(records_dir):
            os.makedirs(records_dir)  # Create the directory if it doesn't exist

        pdf_files = [f for f in os.listdir(records_dir) if f.endswith('.pdf')]
        for pdf_file in pdf_files:
            item = QListWidgetItem(pdf_file)
            self.file_list.addItem(item)

    def load_selected_pdf(self, item):
        """Loads the selected PDF from the list."""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        records_dir = os.path.join(script_dir, 'records')
        file_path = os.path.join(records_dir, item.text())
        self.load_pdf(file_path)

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open PDF File", "", "PDF Files (*.pdf)")
        if file_name:
            self.load_pdf(file_name)

    def close_file(self):
        self.pdf_document = None
        self.pdf_label.clear()

    def load_pdf(self, file_name):
        self.pdf_document = fitz.open(file_name)
        self.current_page = 0
        self.total_pages = self.pdf_document.page_count  # Get total number of pages
        self.zoom_factor = 1.0
        self.display_page()

    def display_page(self):
        if self.pdf_document:
            page = self.pdf_document.load_page(self.current_page)
            pixmap = page.get_pixmap(matrix=fitz.Matrix(self.zoom_factor, self.zoom_factor))

            # Convert the PyMuPDF pixmap to a QImage for displaying in QLabel
            image_format = QImage.Format_RGB888 if pixmap.n < 4 else QImage.Format_RGBA8888
            image = QImage(pixmap.samples, pixmap.width, pixmap.height, pixmap.stride, image_format)

            self.pdf_label.setPixmap(QPixmap.fromImage(image))
            self.pdf_label.adjustSize()

    def zoom_in(self):
        self.zoom_factor += 0.1
        self.display_page()

    def zoom_out(self):
        self.zoom_factor = max(0.1, self.zoom_factor - 0.1)
        self.display_page()

    def fit_to_width(self):
        if self.pdf_document:
            page = self.pdf_document.load_page(self.current_page)
            page_width = page.rect.width
            self.zoom_factor = self.scroll_area.width() / page_width
            self.display_page()

    def next_page(self):
        """Go to the next page."""
        if self.pdf_document and self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.display_page()
        else:
            QMessageBox.information(self, 'End of Document', 'You are on the last page.')

    def prev_page(self):
        """Go to the previous page."""
        if self.pdf_document and self.current_page > 0:
            self.current_page -= 1
            self.display_page()
        else:
            QMessageBox.information(self, 'Beginning of Document', 'You are on the first page.')

    def adjust_navigation_boxes(self, event=None):
        """Reposition navigation boxes on window resize."""
        self.prev_box.setGeometry(285, self.height() // 2 - 25, 120, 50)  # Adjust left box, 25px into viewable area
        self.next_box.setGeometry(self.width() - 155, self.height() // 2 - 25, 120, 50)  # Adjust right box, 25px into viewable area

    def wheelEvent(self, event):
        """Zoom in/out if Ctrl is pressed while scrolling."""
        if event.modifiers() == Qt.ControlModifier:
            if event.angleDelta().y() > 0:
                self.zoom_in()
            else:
                self.zoom_out()

    def toggle_dark_mode(self):
        """Toggle between Dark Mode and Light Mode."""
        if not self.dark_mode:
            # Apply dark mode
            self.setStyleSheet("""
                QMainWindow { background-color: #2e2e2e; color: white; }
                QListWidget { background-color: #3c3c3c; color: white; }
                QLabel { color: white; }
                QScrollArea { background-color: #2e2e2e; }
                QMenuBar { background-color: #3c3c3c; color: white; }
                QMenu { background-color: #3c3c3c; color: white; }
            """)
            self.dark_mode_action.setText('Light Mode')  # Update menu to say "Light Mode"
            self.dark_mode = True
        else:
            # Revert to light mode
            self.setStyleSheet("")
            self.dark_mode_action.setText('Dark Mode')  # Update menu to say "Dark Mode"
            self.dark_mode = False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = PDFViewer()
    viewer.show()
    sys.exit(app.exec_())
