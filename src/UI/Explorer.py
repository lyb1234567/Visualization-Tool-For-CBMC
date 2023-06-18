from PyQt5.QtWidgets import  QMenu,  QInputDialog, QTreeView, QWidget, QFileSystemModel,QMessageBox,QLineEdit
from PyQt5.QtCore import QDir,Qt
import os
import sys
root_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_folder)
from UI.utils import extract_file_name
from UI.TextEdit import TextEdit
from UI.utils import extract_file_name_without_extension
from JsonViwer.MainJsonWindow import MainWindow as jsonWindow
class ExplorerWidget(QWidget):
    def __init__(self,window):
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
        self.window=window
        self.jsonwindow=None

    def handleItemClicked(self, index):
        file_path = self.model.filePath(index)
        if self.model.isDir(index):
            self.treeView.expand(index)
        else:
            if file_path not in self.check_file_lst:
                self.window.openFile(file_path)
                self.check_file_lst.append(file_path)
            else:
                self.window.switchToFile(file_path)

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
                menu.addAction('Delete Folder', lambda: self.deleteFolder(index))
            else:
                menu.addAction("Rename File", lambda: self.renameFile(index))
                menu.addAction("Delete File", lambda: self.deleteFile(index))
                if (file_path.endswith('.json')):
                    menu.addAction("load", lambda: self.loadjson(index))
            menu.exec_(self.treeView.viewport().mapToGlobal(position))


    def loadjson(self,index):
        filePath=self.model.filePath(index)
        if not self.jsonwindow:
            self.jsonwindow=jsonWindow(filePath)
        self.jsonwindow.show()
        
        
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
            textEdit = TextEdit(self.window)  # create TextEdit instance
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
    def deleteFile(self,index):
        file_path = self.model.filePath(index)
        filename=extract_file_name(file_path)
        result = QMessageBox.question(self, "Confirmation", 
                                       f"Are you sure you want to delete' {filename} '?",
                                       QMessageBox.Yes | QMessageBox.No)
        if result == QMessageBox.Yes:
            os.remove(file_path)
            self.window.closeTabdelete(file_path)
    def deleteFolder(self,index):
        dir_path = self.model.filePath(index)
        dir_name=extract_file_name_without_extension(dir_path)
        result = QMessageBox.question(self, "Confirmation", 
                                       f"Are you sure you want to delete' {dir_name} '?",
                                       QMessageBox.Yes | QMessageBox.No)
        if result == QMessageBox.Yes:
            dir_obj = QDir(dir_path)
            if dir_obj.removeRecursively():
                print(f"Folder '{dir_name}' removed successfully.")
            else:
                QMessageBox.warning(self, "Remove Folder", "Failed to remove the folder.")
    
    