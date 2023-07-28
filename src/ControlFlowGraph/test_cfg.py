import os
import sys
root_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_folder)
from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QTextBrowser, QSplitter, QVBoxLayout, QHBoxLayout,QListWidget
from PyQt5.QtCore import Qt
from  UI.Explorer import ExplorerWidget  # 这里我们导入你的 ExplorerWidget

class CustomWidget(QWidget):
    def __init__(self, parent=None):
        super(CustomWidget, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.text_edit = QTextEdit()
        self.list_widget = QListWidget()

        # Add some items to the list widget
        self.list_widget.addItem("Item 1")
        self.list_widget.addItem("Item 2")
        self.list_widget.addItem("Item 3")

        # Create the explorer widget
        self.explorer_widget = ExplorerWidget(self)

        # Create the splitter for right widgets and add widgets
        right_splitter = QSplitter(Qt.Vertical)
        right_splitter.addWidget(self.text_edit)
        right_splitter.addWidget(self.list_widget)

        # Create a QSplitter for all widgets
        main_splitter = QSplitter(Qt.Horizontal)
        main_splitter.addWidget(self.explorer_widget)
        main_splitter.addWidget(right_splitter)

        # Give the explorer widget more space
        main_splitter.setStretchFactor(0, 1)
        main_splitter.setStretchFactor(1, 0)

        # Create the layout and add the splitter
        layout = QVBoxLayout()
        layout.addWidget(main_splitter, stretch=1)  # Give the splitter a larger stretch factor

        # Set the layout
        self.setLayout(layout)

def main():
    app = QApplication([])
    widget = CustomWidget()
    widget.show()
    app.exec_()

if __name__ == "__main__":
    main()
