import sys
import json
import glob
from PyQt5.QtWidgets import (QMainWindow, QComboBox, QVBoxLayout, 
                             QWidget, QFileDialog,
                             QLabel, QStackedLayout,QHBoxLayout,QMenu,QMenuBar,QAction,QInputDialog,QLineEdit,QMessageBox,QListWidget,QListWidgetItem,QDialog)
import os
import sys
root_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_folder)

from JsonViwer.TreeViewer import TreeViewer
from JsonViwer.TextViewer import TextViewer
from JsonViwer.KeysDialog import KeyListDialog
class MainWindow(QMainWindow):
    def __init__(self,filePath=None,editor_window=None):
        super().__init__()
        self.filePath=filePath
        self.editor_window=editor_window
        self.initUI()
        if filePath:
            self.loadJSON()

    def initUI(self):
        self.setGeometry(300, 300, 600, 500)
        self.setWindowTitle('JSON Viewer')

        self.checkLoad=False
        # Create QMenuBar
        self.menuBar = QMenuBar(self)

        # Create menus
        self.fileMenu = QMenu("File", self)
        self.searchMenu = QMenu("Search", self)  # Placeholder for your custom menu
        self.ViewMenu=QMenu("View")
        # Create actions
        self.loadAction = QAction("Load JSON", self)
        self.loadAction.triggered.connect(self.loadJSON)
    
        self.searchByKeyAction = QAction("Search By Key", self)  # Placeholder for your custom action
        self.searchByKeyAction.triggered.connect(self.search)

        self.ViewFailureAction=QAction("View Failure Action")
        self.ViewFailureAction.triggered.connect(self.viewfailure)
        
        self.ViewTraceAction=QAction("View traces")
        self.ViewTraceAction.triggered.connect(self.viewtraces)

        self.formatdict={}
        # Add actions to menus
        self.fileMenu.addAction(self.loadAction)
        self.searchMenu.addAction(self.searchByKeyAction)
        self.ViewMenu.addAction(self.ViewFailureAction)
        self.ViewMenu.addAction(self.ViewTraceAction)
        # Add menus to menuBar
        self.menuBar.addMenu(self.fileMenu)
        self.menuBar.addMenu(self.searchMenu)
        self.menuBar.addMenu(self.ViewMenu)

        # Set menuBar to the mainWindow
        self.setMenuBar(self.menuBar)

        if self.filePath:
            self.treeViewer = TreeViewer(self.editor_window,self,filePath=self.filePath)
        else:
            self.treeViewer = TreeViewer(self.editor_window,self)
        self.textViewer = TextViewer()

        self.stackedLayout = QStackedLayout()
        self.stackedLayout.addWidget(self.treeViewer)
        self.stackedLayout.addWidget(self.textViewer)

        self.formatComboBox = QComboBox(self)
        self.formatComboBox.addItem('Tree')
        self.formatdict[0]="Tree"
        self.formatComboBox.addItem('Text')
        self.formatdict[1]="Text"
        self.formatComboBox.currentIndexChanged.connect(self.switchView)

        self.viewWidget = QWidget()
        self.viewLayout = QVBoxLayout(self.viewWidget)
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel('Format:'))
        hbox.addWidget(self.formatComboBox)
        hbox.addStretch()
        self.viewLayout.addLayout(hbox)

        layoutWidget = QWidget()
        layoutWidget.setLayout(self.stackedLayout)
        self.viewLayout.addWidget(layoutWidget)

        self.setCentralWidget(self.viewWidget)
    def closeEvent(self, event):
        self.checkLoad = False
        event.accept()  # let the window close
    def viewtraces(self):
        current=self.formatdict[self.formatComboBox.currentIndex()]
        if not self.checkLoad:
            QMessageBox.warning(self,"Warning", "There is no file loaded")
        if current=="Tree" and self.checkLoad:
            self.treeViewer.viewtraces() 
        elif current=="Text" and self.checkLoad:
            QMessageBox.critical(self,"Failure", "Viewing failure only works for Tree !!!")
    def viewfailure(self):
        current=self.formatdict[self.formatComboBox.currentIndex()]
        if not self.checkLoad:
            QMessageBox.warning(self,"Warning", "There is no file loaded")
        if current=="Tree" and self.checkLoad:
            if self.treeViewer.FailureList:
                self.treeViewer.viewFailure()
            else:
                QMessageBox.information (self,"Success", "Verification Successful!!")
        elif current=="Text" and self.checkLoad:
            QMessageBox.critical(self,"Failure", "Viewing failure only works for Tree !!!")
    def switchView(self):
        self.stackedLayout.setCurrentIndex(self.formatComboBox.currentIndex())
        
    def loadJSON(self):
        options = QFileDialog.Options()
        if not self.filePath:
            fileName, _ = QFileDialog.getOpenFileName(self,"Load JSON", "","JSON Files (*.json)", options=options)
            self.filePath=fileName
            self.treeViewer.setFilePath(fileName)
        else:
            fileName=self.filePath
        if fileName:
            self.checkLoad=True
            with open(fileName, 'r') as file:
                json_content = json.load(file)
                self.treeViewer.clear()
                self.textViewer.clear()
                self.treeViewer.display(json_content)
                self.textViewer.display(json_content)
                self.filePath=None
                if hasattr(self, 'ViewCounterExamplesAction'):  # Check if the attribute exists
                    self.ViewMenu.removeAction(self.ViewCounterExamplesAction)  # If it does, remove the action
                if (fileName.endswith("trace.json")):
                    self.ViewCounterExamplesAction=QAction("View CounterExamples")
                    self.ViewCounterExamplesAction.triggered.connect(self.treeViewer.viewcounterexamples)
                    self.ViewMenu.addAction(self.ViewCounterExamplesAction)
                    self.treeViewer.ExpandAllCounterExamples()
                else:
                    if not self.treeViewer.FailureList :
                        QMessageBox.information(self,"Success", "Verification Successful")
                    else:
                        self.treeViewer.ExpandAllFailure()
                        QMessageBox.critical(self,"Failure", "{0} failed cases!!".format(len(self.treeViewer.FailureList)))
    def search(self):
        current=self.formatdict[self.formatComboBox.currentIndex()]
        if not self.checkLoad:
            QMessageBox.warning(self,"Warning", "There is no file loaded")
        if current=="Tree" and self.checkLoad:
            OuterKeys=self.treeViewer.insertOuterKeys
            OuterDict=self.treeViewer.OutKeyDict
            dialog = KeyListDialog(OuterKeys, OuterDict,self)
            result = dialog.exec_()
            if result == QDialog.Accepted:
              searchQuery = dialog.selected_key
              searchQueryOrder=int(dialog.selected_keyorder)-1
              self.treeViewer.search(searchQuery,False,searchQueryOrder)
        elif current=="Text" and self.checkLoad:
            QMessageBox.warning(self,"Warning", "Search only works for Tree Viewer !!!")


