from PyQt5.QtWidgets import QMainWindow, QTextEdit, QVBoxLayout, QApplication, QWidget
import sys
class TextFileViewer(QMainWindow):
    def __init__(self, filepath, parent=None):
        super(TextFileViewer, self).__init__(parent)

        # Setup the QTextEdit widget
        self.text_widget = QTextEdit()
        self.text_widget.setReadOnly(True)

        # Load the file contents into the QTextEdit widget
        with open(filepath, 'r') as f:
            file_contents = f.read()
            self.text_widget.setText(file_contents)

        # Setup the QVBoxLayout to use as the window layout
        layout = QVBoxLayout()

        # Add the QTextEdit widget to the layout
        layout.addWidget(self.text_widget)

        # Create a QWidget and set the layout
        central_widget = QWidget()
        central_widget.setLayout(layout)

        # Set the QWidget as the central widget of the QMainWindow
        self.setCentralWidget(central_widget)
