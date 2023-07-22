
from PyQt5.QtGui import QTextCursor
from PyQt5.QtGui import QColor, QTextCursor, QTextCharFormat, QSyntaxHighlighter
from PyQt5.QtWidgets import QTextEdit,QToolTip
from PyQt5.QtCore import QEvent
from ControlFlowGraph.ControlFlowGraphGenerator import Source_Type

class MyHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None,SOURCE_TYPE=None):
        super(MyHighlighter, self).__init__(parent)
        self.highlight_line_number = -1
        self.highlight_format = QTextCharFormat()
        self.source_type=SOURCE_TYPE
        self.set_highlight_type()
    def highlightBlock(self, text):
        if self.currentBlock().blockNumber() == self.highlight_line_number:
            self.setFormat(0, len(text), self.highlight_format)
    def set_highlight_type(self):
            if self.source_type == Source_Type.FAILURE_SOURCE:
                self.highlight_format.setUnderlineStyle(QTextCharFormat.WaveUnderline)  # Set underline style as wave
                self.highlight_format.setUnderlineColor(QColor("red"))  # Set underline color as red
            elif self.source_type == Source_Type.TRACE_SOURCE:
                self.highlight_format.setBackground(QColor("red"))  # Set background color as red
    def highlight_line(self, line_number):
        self.highlight_line_number = line_number
        self.rehighlight()


class TextEdit(QTextEdit):
    def __init__(self,window,line_number=None,counterexamples=None,SOURCE_TYPE=None):
        super().__init__()
        self.fileName = ''
        self.textChanged.connect(self.handleTextChanged)
        self.window=window
        self.line_number=line_number
        self.highlighter = MyHighlighter(self.document(),SOURCE_TYPE=SOURCE_TYPE)
        self.counterexamples=counterexamples
    def event(self, event):
        if (event.type() == QEvent.ToolTip):
            pos = event.pos()
            # Get a QTextCursor at the mouse position
            cursor = self.cursorForPosition(pos)
            # Pass this cursor to the isTextHighlighted method
            if self.isTextHighlighted(cursor):
                block = cursor.block()
                position_in_line = cursor.position()
                range=self.get_line_positions(self.highlighter.highlight_line_number)
                if position_in_line>=range[0] and position_in_line<=range[1]:
                    counterexamplemessage=str(self.highlighter.highlight_line_number+1)
                    QToolTip.showText(event.globalPos(), counterexamplemessage)

            else:
                QToolTip.hideText()
            return True
        return super().event(event)

    def isTextHighlighted(self, cursor):
        # Get the line number of the block that the cursor is in
        line_number = cursor.blockNumber()

        # Return True if the current line is the highlighted line
        return line_number == self.highlighter.highlight_line_number


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
    def get_line_positions(self, line_number):
        # Create a new QTextCursor attached to the QTextEdit document
        cursor = QTextCursor(self.document())

        # Move the cursor to the start of the document
        cursor.movePosition(QTextCursor.Start)

        # Move down by line_number - 1 lines (zero-based)
        for _ in range(line_number):
            cursor.movePosition(QTextCursor.Down)

        # Select the line text
        cursor.select(QTextCursor.LineUnderCursor)
        line_text = cursor.selectedText()

        # Move the cursor to the end of the line
        cursor.movePosition(QTextCursor.EndOfLine)

        # The ending position is the current position of the cursor
        end_position = cursor.position()
        start_position=end_position-len(line_text.strip())
        return start_position, end_position-1
    def counterexamplemessgae(self):
        messages = []
        if self.counterexamples:
            for key, values in self.counterexamples.items():
                value_str = " and ".join(str(value) for value in values)
                messages.append(f"{key} is {value_str}")
        message = "Property Violated, when " + ", ".join(messages)
        return message
    def get_line_text(self, line_number):
        """Get the text of a specific line in the QTextEdit."""
        # Create a new QTextCursor attached to the QTextEdit document
        cursor = QTextCursor(self.document())

        # Move the cursor to the start of the document
        cursor.movePosition(QTextCursor.Start)

        # Move down by line_number - 1 lines (zero-based)
        for _ in range(line_number - 1):
            cursor.movePosition(QTextCursor.Down)

        # Select the text until the end of the line
        cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)

        # Return the selected text
        return cursor.selectedText()