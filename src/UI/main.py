import os
import sys
root_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_folder)
from PyQt5.QtWidgets import QApplication
from UI.MainWindow import MainWindow
app = QApplication([])
window = MainWindow()
window.show()
app.exec_()