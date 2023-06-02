from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QMenu, QAction, QFileDialog, QTextEdit, QInputDialog, QTabWidget, QTreeView, QWidget, QDockWidget, QFileSystemModel

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QDir,Qt
from utils import extract_file_name
import os

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

from PyQt5.QtWidgets import QMenu, QLineEdit, QMessageBox

class ExplorerWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.treeView = QTreeView(self)
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.currentPath())
        self.treeView.setModel(self.model)
        self.treeView.setRootIndex(self.model.index(QDir.currentPath()))
        self.treeView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.showContextMenu)
        self.treeView.clicked.connect(self.handleItemClicked)
        self.check_file_lst=[]

    def handleItemClicked(self, index):
        file_path = self.model.filePath(index)
        if self.model.isDir(index):
            self.treeView.expand(index)
        else:
            if file_path not in self.check_file_lst:
                window.openFile(file_path)
                self.check_file_lst.append(file_path)

    def getFilesInFolder(self, folder_path):
        folder_model = QFileSystemModel()
        folder_model.setRootPath(folder_path)
        file_list = []
        for i in range(folder_model.rowCount()):
            child_index = folder_model.index(i, 0)
            file_name = folder_model.fileName(child_index)
            file_list.append(file_name)
        return file_list

    def showContextMenu(self, position):
        index = self.treeView.indexAt(position)
        file_path = self.model.filePath(index)
        if index.isValid():
            menu = QMenu(self)
            if self.model.isDir(index):
                menu.addAction("Rename Folder", lambda: self.renameFolder(index))
                menu.addAction('Create File', lambda: self.createFile(index))
            else:
                menu.addAction("Rename File", lambda: self.renameFile(index))
            menu.exec_(self.treeView.viewport().mapToGlobal(position))

    def renameFolder(self, index):
        old_name = self.model.filePath(index)
        old_name=extract_file_name(old_name)
        new_name, ok = QInputDialog.getText(self, "Rename Folder", "Enter new folder name:", QLineEdit.Normal, old_name)
        if ok and new_name:
            new_name = new_name.strip()
            if new_name != old_name:
                new_dir = QDir(self.model.filePath(index.parent())).filePath(new_name)
                if not QDir(self.model.filePath(index.parent())).rename(old_name, new_dir):
                    QMessageBox.warning(self, "Rename Folder", "Failed to rename the folder.")
    def createFile(self,index):
        folder_name = self.model.filePath(index)
        fileName, ok = QInputDialog.getText(self, 'New File', 'Enter file name (e.g. file.c or file.json):')
        if ok and fileName:
            if os.path.exists(fileName):
                return
            textEdit = TextEdit()  # create TextEdit instance
            with open(folder_name+'/'+fileName, 'w') as f:  # create an empty file
                pass
            
    
    def renameFile(self, index):
        old_name = self.model.filePath(index)
        old_name=extract_file_name(old_name)
        new_name, ok = QInputDialog.getText(self, "Rename File", "Enter new file name:", QLineEdit.Normal, old_name)
        if ok and new_name:
            new_name = new_name.strip()
            if new_name != old_name:
                new_file = QDir(self.model.filePath(index.parent())).filePath(new_name)
                if not QDir(self.model.filePath(index.parent())).rename(old_name, new_file):
                    QMessageBox.warning(self, "Rename File", "Failed to rename the file.")


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

        self.setupExplorer()

    def setupExplorer(self):
        explorerWidget = ExplorerWidget()
        dockWidget = self.createDockWidget('Explorer', explorerWidget)
        self.addDockWidget(1, dockWidget)

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

        textEdit = TextEdit()
        with open(file_path, 'r') as f:
            fileData = f.read()
        textEdit.setText(fileData)
        textEdit.fileName = file_path
        fileName = extract_file_name(file_path)
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
            fileName = extract_file_name(fileName)
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
