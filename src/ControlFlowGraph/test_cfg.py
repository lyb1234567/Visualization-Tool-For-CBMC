from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QDialog
from PyQt5.QtGui import QTextCursor
from PyQt5.QtCore import Qt, QEvent

class TextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.text = ''
    
    def setText(self, text):
        super().setText(text)
        self.text = text


class SearchDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Search')
        self.text_edit = parent.text_edit

        self.search_box = QLineEdit(self)
        self.search_box.textChanged.connect(self.perform_search)  # change here

        self.next_button = QPushButton('↓', self)
        self.next_button.clicked.connect(self.perform_search_next)

        self.previous_button = QPushButton('↑', self)
        self.previous_button.clicked.connect(self.perform_search_previous)

        self.match_label = QLabel(self)

        search_layout = QHBoxLayout()
        search_layout.addWidget(self.search_box)
        search_layout.addWidget(self.next_button)
        search_layout.addWidget(self.previous_button)
        search_layout.addWidget(self.match_label)

        layout = QVBoxLayout(self)
        layout.addLayout(search_layout)

        self.matches = []
        self.current_match = -1
    def perform_search(self):
        self.matches.clear()
        self.current_match = -1
        self.text_edit.moveCursor(QTextCursor.Start)
        search_term = self.search_box.text()
        while self.text_edit.find(search_term):
            cursor = self.text_edit.textCursor()
            self.matches.append((cursor.position() - len(search_term), cursor.position()))
        if self.matches:
            self.current_match = 0
            self.highlight_match()
        self.update_match_label()

    def perform_search_next(self):
        if not self.matches:
            return
        self.current_match = (self.current_match + 1) % len(self.matches)
        self.highlight_match()
        self.update_match_label()

    def perform_search_previous(self):
        if not self.matches:
            return
        self.current_match = (self.current_match - 1) % len(self.matches)
        self.highlight_match()
        self.update_match_label()

    def highlight_match(self):
        start, end = self.matches[self.current_match]
        cursor = self.text_edit.textCursor()
        cursor.setPosition(start)
        cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, end - start)
        self.text_edit.setTextCursor(cursor)

    def update_match_label(self):
        if not self.matches:
            self.match_label.setText('No results')
        else:
            self.match_label.setText(f'{self.current_match + 1} of {len(self.matches)}')

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.text_edit = TextEdit(self)
        self.text_edit.setText("Sample Text for Testing the Search Functionality.")
        self.setCentralWidget(self.text_edit)

        self.search_dialog = SearchDialog(self)
        self.search_dialog.hide()

        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj is self and event.type() == QEvent.KeyPress and event.key() == Qt.Key_F and event.modifiers() == Qt.ControlModifier:
            self.search_dialog.setVisible(not self.search_dialog.isVisible())
            return True
        return super().eventFilter(obj, event)

def main():
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec_()

if __name__ == '__main__':
    main()

