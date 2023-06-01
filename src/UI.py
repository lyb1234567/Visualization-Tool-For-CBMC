from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QMenu, QAction, QFileDialog, QTextEdit, QInputDialog, QTabWidget
import os
from utils import extract_file_name
class TextEdit(QTextEdit):
    def __init__(self):
        super().__init__()
        self.fileName = ''
        self.textChanged.connect(self.handleTextChanged)

    def handleTextChanged(self):
        currentIndex = window.tabWidget.currentIndex()
        currentTitle = window.tabWidget.tabText(currentIndex)
        if not currentTitle.endswith('*'):
            window.tabWidget.setTabText(currentIndex, currentTitle+'*')


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 600)

        self.tabWidget = QTabWidget()
        self.setCentralWidget(self.tabWidget)

        self.tabWidget.setTabsClosable(True)
        self.tabWidget.tabCloseRequested.connect(self.closeTab)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')

        openFile = QAction('Open File', self)
        openFile.setShortcut('Ctrl+O')
        openFile.triggered.connect(self.openFile)
        fileMenu.addAction(openFile)

        # openFolder=QAction('Open Folder',self)
        # openFolder.setShortcuts(['Ctrl+K','Ctrl+O'])
        # openFolder.triggered.connect(self.openFolder)
        # fileMenu.addAction(openFolder)
        

        createFile = QAction('Create File', self)
        createFile.setShortcut('Ctrl+N')
        createFile.triggered.connect(self.createFile)
        fileMenu.addAction(createFile)

        saveFile = QAction('Save', self)
        saveFile.setShortcut('Ctrl+S')
        saveFile.triggered.connect(self.saveFile)
        fileMenu.addAction(saveFile)

        closeTab = QAction('Close Tab', self)
        closeTab.setShortcut('Ctrl+W')
        closeTab.triggered.connect(self.closeTab)
        fileMenu.addAction(closeTab)
        
        
    def openFolder(self):
        pass 
    def openFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'C Files (*.c);;JSON Files (*.json)', options=options)
        if fileName:
            textEdit = TextEdit()
            with open(fileName, 'r') as f:
                fileData = f.read()
            textEdit.setText(fileData)
            textEdit.fileName = fileName
            fileName=extract_file_name(fileName)
            self.tabWidget.addTab(textEdit, fileName)

    def createFile(self):
        fileName, ok = QInputDialog.getText(self, 'New File', 'Enter file name (e.g. file.c or file.json):')
        if ok and fileName:
            if os.path.exists(fileName):
                return
            textEdit = TextEdit()  # create TextEdit instance
            with open(fileName, 'w') as f:  # create an empty file
                pass
            textEdit.fileName = fileName
            fileName=extract_file_name(fileName)
            self.tabWidget.addTab(textEdit, fileName)

    def saveFile(self):
        textEdit = self.tabWidget.currentWidget()
        if textEdit and textEdit.fileName:
            with open(textEdit.fileName, 'w') as f:
                f.write(textEdit.toPlainText())
            currentIndex = self.tabWidget.currentIndex()
            currentTitle = self.tabWidget.tabText(currentIndex)
            if currentTitle.endswith('*'):
                self.tabWidget.setTabText(currentIndex, currentTitle[0:len(currentTitle)-1])
        elif textEdit:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            fileName, _ = QFileDialog.getSaveFileName(self, 'Save File', '', 'C Files (*.c);;JSON Files (*.json)', options=options)
            if fileName:
                with open(fileName, 'w') as f:
                    f.write(textEdit.toPlainText())
                currentIndex = self.tabWidget.currentIndex()
                self.tabWidget.setTabText(currentIndex, fileName)
                textEdit.fileName = fileName

    def closeTab(self, index):
        self.tabWidget.removeTab(index)


app = QApplication([])
window = MainWindow()
window.show()
app.exec_()
