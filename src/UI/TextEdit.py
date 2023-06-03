from PyQt5.QtWidgets import QTextEdit
class TextEdit(QTextEdit):
    def __init__(self,window):
        super().__init__()
        self.fileName = ''
        self.textChanged.connect(self.handleTextChanged)
        self.window=window

    def handleTextChanged(self):
        currentIndex = self.window.tabWidget.currentIndex()
        currentTitle = self.window.tabWidget.tabText(currentIndex)
        if not currentTitle.endswith('*'):
           self.window.tabWidget.setTabText(currentIndex, currentTitle+'*')