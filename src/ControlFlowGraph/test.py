from PyQt5.QtWidgets import QApplication, QTextEdit, QMainWindow
from PyQt5.QtGui import QTextCharFormat, QColor

class TextEdit(QTextEdit):
    def __init__(self):
        super().__init__()
        self.text_to_search = ''

    def search_and_highlight(self, text):
        self.text_to_search = text
        self.highlight_all_occurrences()

    def highlight_all_occurrences(self):
        extra_selections = []
        if self.text_to_search:
            highlight_format = QTextCharFormat()
            highlight_format.setBackground(QColor("red"))
            cursor = self.document().find(self.text_to_search)
            while not cursor.isNull():
                selection = QTextEdit.ExtraSelection()
                selection.format = highlight_format
                selection.cursor = cursor
                extra_selections.append(selection)
                cursor = self.document().find(self.text_to_search, cursor.position() + 1)
        self.setExtraSelections(extra_selections)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.text_edit = TextEdit()
        self.setCentralWidget(self.text_edit)
        self.text_edit.setText("This is a test. Testing the highlight function.Here is another test")
        self.text_edit.search_and_highlight("test")

app = QApplication([])
window = MainWindow()
window.show()
app.exec_()