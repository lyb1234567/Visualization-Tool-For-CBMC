import os
import sys
root_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_folder)
from PyQt5.QtWidgets import QMainWindow,QAction, QFileDialog, QInputDialog, QTabWidget, QDockWidget, QFileSystemModel,QVBoxLayout,QWidget,QDialog,QMessageBox
from PyQt5.QtCore import QDir
import subprocess
from UI.utils import extract_file_name,print_result
from UI.TextEdit import TextEdit
from UI.Explorer import ExplorerWidget
from UI.utils import extract_file_name_without_extension
from UI.Terminal import Terminal
from UI.Fileselection import MultiFileDialog
from JsonViwer.MainJsonWindow import MainWindow as jsonWindow
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 600)
        self.mainWidget = QWidget(self)  # Create main widget
        self.setCentralWidget(self.mainWidget)
        self.jsonwindow=None
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
        runMenu=menubar.addMenu("Run")

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

        OpenExplorer=QAction('Open Explorer',self)
        OpenExplorer.triggered.connect(self.openExplorer)
        fileMenu.addAction(OpenExplorer)


        jsonloader=QAction('Load JsonFile',self)
        jsonloader.triggered.connect(self.loadJson)
        fileMenu.addAction(jsonloader)



        TerminalTab=QAction('New Terminal',self)
        TerminalTab.triggered.connect(self.refreshTerminal)
        TerminalMenu.addAction(TerminalTab)
        
        debugTabsingle=QAction("Run current file",self)
        debugTabsingle.triggered.connect(self.runfilesingle)
        runMenu.addAction(debugTabsingle)

        debugTabmultiple=QAction("Run multiple files",self)
        debugTabmultiple.triggered.connect(self.runfilemultiple)
        runMenu.addAction(debugTabmultiple)

        

        self.explorer=self.setupExplorer()
        self.model = QFileSystemModel()
        self.check_tab_lst=[]

    
    def openExplorer(self):
        self.explorer=self.setupExplorer()
    
    def loadJson(self):
        if not self.jsonwindow:
            self.jsonwindow=jsonWindow()
        self.jsonwindow.show()
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
        temp=file_path
        fileName = extract_file_name(file_path)
        if fileName not in  self.check_tab_lst:
            self.tabWidget.addTab(textEdit, fileName)
            self.switchToFile(temp)
            self.check_tab_lst.append(fileName)

    def createFile(self):
        fileName, ok = QInputDialog.getText(self, 'New File', 'Enter file name (e.g. file.c or file.json):')
        temp=fileName
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
            self.switchToFile(temp)
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
    def closeTabdelete(self,fileName):
        for i in range(self.tabWidget.count()):
                print(self.tabWidget.widget(i).fileName)
                if self.tabWidget.widget(i).fileName == fileName:  # Assuming each tab has a filePath attribute
                    self.tabWidget.removeTab(i)
                    break
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
    def runfilesingle(self,index):
        tab = self.tabWidget.widget(index)
        if tab:
            fileName=extract_file_name(tab.fileName)
            command='cbmc {0} --trace --json-ui > {1}.json'.format(fileName,extract_file_name_without_extension(tab.fileName))
            result = subprocess.run([command], shell=True, capture_output=True, text=True)
            print_result(result,self,command)
        else:
            QMessageBox.warning(self, "Choose a file to open!!")
            
    def runfilemultiple(self):
    # get the list of files in the current directory
        current_folder = os.getcwd()
        files = os.listdir(current_folder)  # Get the list of files in the current folder
        # # create and show the dialog
        dialog = MultiFileDialog(files, self)
        result = dialog.exec_()

        # if the user clicked OK, get the selected files and process them
        if result == QDialog.Accepted:
            selected_files = dialog.getSelectedFiles()
        combined_file_name=""

        if selected_files:
           for file in selected_files:
               file=extract_file_name(file)
               combined_file_name=combined_file_name+file+" "
        # TODO: implement the functions of running multiple files in cbmc
        build_goto_file=None
        generate_json_file=None
        outputFile, ok = QInputDialog.getText(self, 'Output file', 'Enter output file name')
        if ok and outputFile:
            build_goto_file="goto-cc "+combined_file_name+"-o "+outputFile
        if build_goto_file:
            subprocess.run([build_goto_file], shell=True, capture_output=True, text=True)
            generate_json_file='cbmc {0} --trace --json-ui > {1}.json'.format(outputFile,outputFile)
        result = subprocess.run([generate_json_file], shell=True, capture_output=True, text=True)
        print_result(result,self,generate_json_file)
        
        
