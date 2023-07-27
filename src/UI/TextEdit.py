
from PyQt5.QtGui import QTextCursor
from PyQt5.QtGui import QColor, QTextCursor, QTextCharFormat, QSyntaxHighlighter,QTextDocument
from PyQt5.QtWidgets import QTextEdit,QToolTip
from PyQt5.QtCore import QEvent
from ControlFlowGraph.ControlFlowGraphGenerator import Source_Type
class SearchHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(SearchHighlighter, self).__init__(parent)
        self.text_to_highlight = ""
        self.highlight_format = QTextCharFormat()
        self.highlight_format.setBackground(QColor("yellow"))  # Set the highlight background to yellow

    def set_highlight_text(self, text):
        
        self.text_to_highlight = text
        self.rehighlight()

    def highlightBlock(self, text):
        if self.text_to_highlight:
            index = text.lower().find(self.text_to_highlight.lower())
            while index >= 0:
                length = len(self.text_to_highlight)
                self.setFormat(index, length, self.highlight_format)
                index = text.lower().find(self.text_to_highlight.lower(), index + length)
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
    def __init__(self,window,line_number=None,counterexamples=None,SOURCE_TYPE=None,cfg=None,trace_num=None,fileName=None,assertion_statement=None):
        super().__init__()
        self.fileName = fileName
        self.textChanged.connect(self.handleTextChanged)
        self.window=window
        self.line_number=line_number
        self.highlighter = MyHighlighter(self.document(),SOURCE_TYPE=SOURCE_TYPE)
        self.counterexamples=counterexamples
        self.cfg=cfg
        self.trace_num=trace_num
        self.text_to_search = ''
        self.assertion_statement=assertion_statement
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
                    # TODO: 当用户鼠标悬停高亮代码的时候，应该得到对应文件中对应行数代码的state information
                    trace_name='trace_'+str(self.trace_num)
                    line_number=self.highlighter.highlight_line_number+1
                    state_info=self.cfg.get_assertion_info(fileName=self.fileName,line_number=self.line_number,assertion_statement=self.assertion_statement)
                    QToolTip.showText(event.globalPos(), state_info)

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
    def search_and_highlight(self, text):
        self.text_to_search = text
        self.highlight_all_occurrences()

    def highlight_all_occurrences(self):
        extra_selections = []
        if self.text_to_search:
            highlight_format = QTextCharFormat()
            highlight_format.setBackground(QColor("yellow"))
            cursor = self.document().find(self.text_to_search)
            while not cursor.isNull():
                selection = QTextEdit.ExtraSelection()
                selection.format = highlight_format
                selection.cursor = cursor
                extra_selections.append(selection)
                cursor = self.document().find(self.text_to_search, cursor.position() + 1)
        self.setExtraSelections(extra_selections)