from PyQt5.QtWidgets import QMainWindow,QAction, QFileDialog, QInputDialog, QTabWidget, QDockWidget, QFileSystemModel,QPlainTextEdit,QVBoxLayout
from PyQt5.QtCore import QProcess,Qt
from PyQt5.QtGui import QTextCursor
import subprocess
from UI.utils import extract_command
class Terminal(QPlainTextEdit):
    def __init__(self, parent=None):
        super(Terminal, self).__init__(parent)
        self.process = QProcess(self)
        self.process.readyRead.connect(self.dataReady)
        self.process.start('cmd.exe')
        welcome_message = "Welcome to the terminal! You can now only use the following commands: xxx \n"
        self.appendPlainText(welcome_message)


    def dataReady(self):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(str(self.process.readAll(), 'utf-8'))
        self.ensureCursorVisible()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            print(self.toPlainText())
            command = self.toPlainText().split('\n')[-2]
            last_command=self.toPlainText().split('\n')[-1]
            last_command=extract_command(last_command)
            
            if last_command.strip() == 'cls'or last_command.strip() == 'CLS':
                self.process.write(command.encode('utf-8'))
                self.process.write(b'\n')
                self.clear()
            else:
                result = subprocess.run([last_command], shell=True, capture_output=True, text=True)
                if result.stdout:
                    self.appendPlainText(result.stdout)
                    self.process.write(b'\n')
                else:
                    self.appendPlainText(result.stderr)
                    self.process.write(b'\n')        
        super(Terminal, self).keyPressEvent(event)