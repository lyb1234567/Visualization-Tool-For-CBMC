import os
import sys
root_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_folder)
from PyQt5.QtWidgets import QMainWindow,QAction, QFileDialog, QInputDialog, QTabWidget, QDockWidget,QSplitter
from PyQt5.QtWidgets import QFileSystemModel,QVBoxLayout,QWidget,QDialog,QMessageBox,QShortcut,QLineEdit,QPushButton,QLabel,QHBoxLayout,QVBoxLayout
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QKeySequence
import subprocess
from UI.utils import extract_file_name,print_result
from UI.TextEdit import TextEdit
from UI.Explorer import ExplorerWidget
from UI.utils import extract_file_name_without_extension,wait_for_file
from UI.Terminal import Terminal
from UI.Fileselection import MultiFileDialog
from UI.SearchDialog import SearchDialog
from UI.Line_Number_Widget import LineNumberWidget
from JsonViwer.MainJsonWindow import MainWindow as jsonWindow
from ControlFlowGraph.ControlFlowGraphGenerator import ControlGraphGenerator
class FileWidget(QWidget):
    def __init__(self, fileName, parent=None,editor_widget=None,line_number_widget=None):
        super(FileWidget, self).__init__(parent)
        self.fileName = fileName
        self.editor=editor_widget
        self.line_number=line_number_widget
    def get_fileName(self):
        return self.fileName
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 600)
        self.mainWidget = QWidget(self)  # Create main widget
        self.setCentralWidget(self.mainWidget)
        self.editor=None
        self.line_number_widget=None
        self.jsonwindow=None
        self.fileChange=False
        self.cfg=None
        self.mainLayout = QVBoxLayout(self.mainWidget)  # Create main layout
        self.splitter = QSplitter()
        self.tabWidget = QTabWidget()
        self.tabWidget.currentChanged.connect(self.on_tab_changed)
        # Add tabWidget to the layout instead of setting it as centralWidget
        self.mainLayout.addWidget(self.tabWidget)
        
        self.terminal = Terminal(editor_window=self)  # Initialize the terminal
        self.mainLayout.addWidget(self.terminal)  # Add the terminal to the layout
        self.find_shortcut = QShortcut(QKeySequence("Ctrl+F"), self)
                # Connect the triggered signal of the shortcut to a slot method
        self.find_shortcut.activated.connect(self.handle_find)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.tabCloseRequested.connect(self.closeTab)

        self.search_dialog = SearchDialog(self)
        self.search_dialog.hide()
        self.installEventFilter(self)


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
        self.counterexmaples={}


    def on_tab_changed(self, index):
        # Get the currently selected TextEdit
        currentTextEdit = self.tabWidget.widget(index)
        fileName = currentTextEdit.fileName if currentTextEdit else None
        # Get the fileName property of the current TextEdit
        # fileName = currentTextEdit.fileName if currentTextEdit else None
        # Now you can use fileName or currentTextEdit for whatever you want
        # For example, if you want to create a new editor for the selected file:
        # if fileName:
        #     self.editor= TextEdit(self,fileName=extract_file_name(fileName))
    def handle_find(self):
        currentTextEdit = self.tabWidget.currentWidget()
        if currentTextEdit:
            self.search_dialog.fileWidget.editor_widget=currentTextEdit
            self.search_dialog.setVisible(not self.search_dialog.isVisible())
    def openExplorer(self):
        self.explorer=self.setupExplorer()
    
    def loadJson(self):
        if not self.jsonwindow:
            self.jsonwindow=jsonWindow(editor_window=self)
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


    def __line_widget_line_count_changed(self):
        if self.line_number_widget:
            n1 = int(self.editor.document().lineCount())
            self.line_number_widget.changeLineCount(n1)
    def openFile(self, file_path=None,line_number=None,SOURCE_TYPE=None,cfg=None,assertion_statement=None):
        if not file_path:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            file_path, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'C Files (*.c);;JSON Files (*.json)', options=options)
            if not file_path:
                return
        self.editor=TextEdit(self,SOURCE_TYPE=SOURCE_TYPE,fileName=extract_file_name(file_path),cfg=cfg,assertion_statement=assertion_statement,line_number=line_number)
        self.editor.textChanged.connect(self.__line_widget_line_count_changed)
        self.line_number_widget=LineNumberWidget(widget=self.editor,fileName=extract_file_name(file_path))
        new_file_widget=FileWidget(fileName=extract_file_name(file_path),editor_widget=self.editor,line_number_widget=self.line_number_widget)
        new_layout=QHBoxLayout(new_file_widget)
        new_layout.addWidget(self.line_number_widget)
        new_layout.addWidget(self.editor)
        self.search_dialog.fileWidget=new_file_widget
        try:
            with open(file_path, 'r') as f:
                fileData = f.read()  
                self.editor.setPlainText(fileData)
                if line_number:
                    tab_index=self.get_tabindex(file_path)
                    if tab_index !=None:
                        self.closeTab(tab_index)
                    self.editor.highlight_line(int(line_number))
                    # textEdit.counterexamples=self.counterexmaples[file_path]
                self.editor.fileName = file_path
                temp=file_path
                fileName = extract_file_name(file_path)
                if fileName not in  self.check_tab_lst:
                    self.tabWidget.addTab(new_file_widget, fileName)
                    self.switchToFile(temp)
                    self.check_tab_lst.append(fileName)
        except UnicodeDecodeError:
        # 文件存在，但是格式不正确
                 QMessageBox.warning(self,"Warning", "Wrong format")
        except FileNotFoundError:
        # 文件不存在
                 QMessageBox.warning(self,"Warning", "There is no such file in the directory!!")

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
        else:
            pass

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
        fileName=tab.get_fileName()
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
        self.terminal = Terminal(editor_window=self)  # Initialize the terminal
        self.mainLayout.addWidget(self.terminal)  # Add the terminal to the layout
    def switchToFile(self,file_path):
        for i in range(self.tabWidget.count()):
            tab = self.tabWidget.widget(i)
            if tab.fileName == extract_file_name(file_path):
                self.tabWidget.setCurrentWidget(tab)
                break
    def runfilesingle(self,index):
        tab = self.tabWidget.widget(index)
        if tab:
            fileName=extract_file_name(tab.fileName)
            command_1='cbmc {0} --trace --json-ui > {1}.json'.format(fileName,extract_file_name_without_extension(tab.fileName))
            command_2='cbmc {0} --trace > trace.txt'.format(fileName,extract_file_name_without_extension(tab.fileName))
            result = subprocess.run([command_1], shell=True, capture_output=True, text=True)
            subprocess.run([command_2], shell=True, capture_output=True, text=True)
            jsonfile="{0}.json".format(extract_file_name_without_extension(tab.fileName))
            self.cfg=ControlGraphGenerator(trace_file='trace.txt')
            if (os.path.exists(jsonfile)):
                if not self.jsonwindow or  self.jsonFileChange:
                    self.jsonwindow=jsonWindow(jsonfile,editor_window=self,cfg=self.cfg,run_by_editor=True)
                    self.jsonFileChange=True
                    self.jsonwindow.treeViewer.ExpandAllFailure()
                    self.jsonwindow.show()
            print_result(result,self,command_1)
        else:
            QMessageBox.warning(self,"Warning", "Choose a file to open!!")
    
    def get_tabindex(self,fileName):
        for i in range(self.tabWidget.count()):
            tab = self.tabWidget.widget(i)
            if extract_file_name(tab.fileName)==fileName:
                return i
        return None
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
        else:
            selected_files=None
        combined_file_name=""

        if selected_files and len(selected_files)>1:
            for file in selected_files:
                file=extract_file_name(file)
                combined_file_name=combined_file_name+file+" "
            build_goto_file=None
            generate_json_file=None
            outputFile, ok = QInputDialog.getText(self, 'Output file', 'Enter output file name')
            if ok and outputFile:
                build_goto_file="goto-cc "+combined_file_name+"-o "+outputFile
            if build_goto_file:
                subprocess.run([build_goto_file], shell=True, capture_output=True, text=True)
                generate_json_file='cbmc {0} --trace --json-ui > {1}.json'.format(outputFile,outputFile)
                generate_trace_file='cbmc {0} --trace  > trace.txt'.format(outputFile,outputFile)
            result = subprocess.run([generate_json_file], shell=True, capture_output=True, text=True)
            subprocess.run([generate_trace_file], shell=True, capture_output=True, text=True)
            print_result(result,self,generate_json_file)
            jsonfile="{0}.json".format(outputFile)
            wait_for_file(jsonfile)
            self.cfg=ControlGraphGenerator(trace_file='trace.txt')
            if os.path.exists(jsonfile):
                if not self.jsonwindow or self.fileChange:
                    self.jsonwindow=jsonWindow(jsonfile,editor_window=self,cfg=self.cfg,run_by_editor=True)
                    self.jsonFileChange=True
                    self.jsonwindow.show()
        elif selected_files and len(selected_files)==1:
            fileName=selected_files[0]
            command_1='cbmc {0} --trace --json-ui > {1}.json'.format(fileName,extract_file_name_without_extension(fileName))
            command_2='cbmc {0} --trace > trace.txt'.format(fileName,extract_file_name_without_extension(fileName))
            result = subprocess.run([command_1], shell=True, capture_output=True, text=True)
            subprocess.run([command_2], shell=True, capture_output=True, text=True)
            jsonfile="{0}.json".format(extract_file_name_without_extension(fileName))
            self.cfg=ControlGraphGenerator(trace_file='trace.txt')
            if (os.path.exists(jsonfile)):
                if not self.jsonwindow or  self.jsonFileChange:
                    self.jsonwindow=jsonWindow(jsonfile,editor_window=self,cfg=self.cfg,run_by_editor=True)
                    self.jsonFileChange=True
                    self.jsonwindow.treeViewer.ExpandAllFailure()
                    self.jsonwindow.show()
            print_result(result,self,command_1)
        
        
