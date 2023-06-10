import os
import sys
root_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_folder)
from PyQt5.QtWidgets import QMainWindow,QAction, QFileDialog, QInputDialog, QTabWidget, QDockWidget, QFileSystemModel,QPlainTextEdit,QVBoxLayout,QWidget,QSplitter
from PyQt5.QtCore import QProcess,Qt,pyqtSignal
from PyQt5.QtGui import QTextCursor
from UI.utils import extract_file_name,extract_command
from UI.TextEdit import TextEdit
from UI.Explorer import ExplorerWidget
from UI.utils import extract_command
from UI.Terminal import Terminal

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 600)
        self.mainWidget = QWidget(self)  # Create main widget
        self.setCentralWidget(self.mainWidget)

        self.mainLayout = QVBoxLayout(self.mainWidget)  # Create main layout

        self.tabWidget = QTabWidget()

        # Add tabWidget to the layout instead of setting it as centralWidget
        self.mainLayout.addWidget(self.tabWidget)
        
        self.terminal = Terminal()  # Initialize the terminal
        self.mainLayout.addWidget(self.terminal)  # Add the terminal to the layout


    
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.tabCloseRequested.connect(self.closeTab)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        TerminalMenu=menubar.addMenu('Terminal')

        openFile = QAction('Open File', self)
        openFile.setShortcut('Ctrl+O')
        openFile.triggered.connect(self.openFile)
        fileMenu.addAction(openFile)

        openFolder = QAction('Open Folder', self)
        openFolder.setShortcut('Ctrl+Shift+O')
        openFolder.triggered.connect(self.openFolder)
        fileMenu.addAction(openFolder)

        createFile = QAction('Create File', self)
        createFile.setShortcut('Ctrl+N')
        createFile.triggered.connect(self.createFile)
        fileMenu.addAction(createFile)

        createFolder = QAction('Create Folder', self)
        createFolder.setShortcut('Ctrl+Shift+N')
        createFolder.triggered.connect(self.createFolder)
        fileMenu.addAction(createFolder)

        saveFile = QAction('Save', self)
        saveFile.setShortcut('Ctrl+S')
        saveFile.triggered.connect(self.saveFile)
        fileMenu.addAction(saveFile)

        closeTab = QAction('Close Tab', self)
        closeTab.setShortcut('Ctrl+W')
        closeTab.triggered.connect(self.closeTab)
        fileMenu.addAction(closeTab)

        TerminalTab=QAction('New Terminal',self)
        TerminalTab.triggered.connect(self.refreshTerminal)
        TerminalMenu.addAction(TerminalTab)

        self.explorer=self.setupExplorer()
        self.model = QFileSystemModel()
        self.check_tab_lst=[]


    def setupExplorer(self):
        explorerWidget = ExplorerWidget(self)
        dockWidget = self.createDockWidget('Explorer', explorerWidget)
        self.addDockWidget(1, dockWidget)
        return explorerWidget

    def createDockWidget(self, title, widget):
        dockWidget = QDockWidget(title, self)
        dockWidget.setWidget(widget)
        return dockWidget

    def openFile(self, file_path=None):
        if not file_path:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            file_path, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'C Files (*.c);;JSON Files (*.json)', options=options)
            if not file_path:
                return

        textEdit = TextEdit(self)
        with open(file_path, 'r') as f:
            fileData = f.read()
        textEdit.setText(fileData)
        textEdit.fileName = file_path
        fileName = extract_file_name(file_path)
        if fileName not in  self.check_tab_lst:
            self.tabWidget.addTab(textEdit, fileName)
            self.check_tab_lst.append(fileName)

    def createFile(self):
        fileName, ok = QInputDialog.getText(self, 'New File', 'Enter file name (e.g. file.c or file.json):')
        if ok and fileName:
            if os.path.exists(fileName):
                return
            textEdit = TextEdit(self)  # create TextEdit instance
            with open(fileName, 'w') as f:  # create an empty file
                pass
            textEdit.fileName = fileName
            fileName = extract_file_name(fileName)
        if fileName not in  self.check_tab_lst:
            self.tabWidget.addTab(textEdit, fileName)
            self.check_tab_lst.append(fileName)

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
        tab = self.tabWidget.widget(index)
        self.tabWidget.removeTab(index)
        self.check_tab_lst.remove(extract_file_name(tab.fileName))
        try:
            self.explorer.check_file_lst.remove(tab.fileName)
        except:
            pass 
    
    def createFolder(self):
        folderName, ok = QInputDialog.getText(self, 'New Folder', 'Enter folder name:')
        if ok and folderName:
            if not os.path.exists(folderName):
                os.makedirs(folderName)
    def openFolder(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Open Folder', '')
        if folder_path:
            self.explorer.openFolder(folder_path)
    def refreshTerminal(self, index):
        self.terminal.deleteLater()
        self.terminal = Terminal()  # Initialize the terminal
        self.mainLayout.addWidget(self.terminal)  # Add the terminal to the layout
    def switchToFile(self,file_path):
        for i in range(self.tabWidget.count()):
            tab = self.tabWidget.widget(i)
            if tab.fileName == file_path:
                self.tabWidget.setCurrentWidget(tab)
                break
        

