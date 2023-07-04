
from PyQt5.QtGui import QTextCursor
from PyQt5.QtGui import QColor, QTextCursor, QTextCharFormat, QSyntaxHighlighter
from PyQt5.QtWidgets import QTextEdit

class MyHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(MyHighlighter, self).__init__(parent)
        self.highlight_line_number = -1
        self.highlight_format = QTextCharFormat()
        self.highlight_format.setUnderlineStyle(QTextCharFormat.WaveUnderline) # Set underline style as wave
        self.highlight_format.setUnderlineColor(QColor("red"))  # Set underline color as red
    def highlightBlock(self, text):
        if self.currentBlock().blockNumber() == self.highlight_line_number:
            self.setFormat(0, len(text), self.highlight_format)

    def highlight_line(self, line_number):
        self.highlight_line_number = line_number
        self.rehighlight()


class TextEdit(QTextEdit):
    def __init__(self,window,line_number=None):
        super().__init__()
        self.fileName = ''
        self.textChanged.connect(self.handleTextChanged)
        self.window=window
        self.line_number=line_number
        self.highlighter = MyHighlighter(self.document())
    def handleTextChanged(self):
        currentIndex = self.window.tabWidget.currentIndex()
        currentTitle = self.window.tabWidget.tabText(currentIndex)
        if not currentTitle.endswith('*'):
           self.window.tabWidget.setTabText(currentIndex, currentTitle+'*')
    def navigate_to_line(self, line_number):
        """Navigate to a specific line in the QTextEdit."""
        # Create a new QTextCursor attached to the QTextEdit document
        cursor = QTextCursor(self.document())
        
        # Move the cursor to the start of the document
        cursor.movePosition(QTextCursor.Start)

        # Move down by line_number - 1 lines (zero-based)
        for _ in range(line_number - 1):
            cursor.movePosition(QTextCursor.Down)

        # Set this new cursor as the active cursor in the QTextEdit
        cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)

        # Set this new cursor as the active cursor in the QTextEdit
        self.setTextCursor(cursor)
    def highlight_line(self, line_number):
        self.highlighter.highlight_line(line_number - 1)
        