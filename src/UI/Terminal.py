from PyQt5.QtWidgets import QMainWindow,QAction, QFileDialog, QInputDialog, QTabWidget, QDockWidget, QFileSystemModel,QPlainTextEdit,QVBoxLayout
from PyQt5.QtCore import QProcess,Qt
from PyQt5.QtGui import QTextCursor
import subprocess
import os
import sys
root_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_folder)
from UI.utils import extract_command,extract_file_name_without_extension
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
            print(last_command)
            if last_command.strip() == 'clear':
                self.process.write(command.encode('utf-8'))
                self.process.write(b'\n')
                self.clear()
            elif last_command.strip().startswith('run'):
                file_lst=last_command.split(' ')[1:]
                if len(file_lst)==1:
                    file_name=extract_file_name_without_extension(file_lst[0])
                    command='cbmc {0} --trace --json-ui > {1}.json'.format(file_lst[0],file_name)
                    result = subprocess.run([command], shell=True, capture_output=True, text=True)
                    if result.stdout:
                        self.appendPlainText(result.stdout)
                        self.process.write(b'\n')
                    elif result.stderr:
                        self.appendPlainText(result.stderr)
                        self.process.write(b'\n')
                    else:
                        self.appendPlainText(command)
                        self.process.write(b'\n')
                else:
                    pass
            else:
                result = subprocess.run([last_command], shell=True, capture_output=True, text=True)
                if result.stdout:
                    self.appendPlainText(result.stdout)
                    self.process.write(b'\n')
                else:
                    self.appendPlainText(result.stderr)
                    self.process.write(b'\n')
        super(Terminal, self).keyPressEvent(event)