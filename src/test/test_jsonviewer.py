import os
import sys
root_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_folder)
from PyQt5.QtWidgets import QApplication
from JsonViwer.MainJsonWindow import MainWindow as jsonWindow
app = QApplication([])
window = jsonWindow()
window.show()
app.exec_() 