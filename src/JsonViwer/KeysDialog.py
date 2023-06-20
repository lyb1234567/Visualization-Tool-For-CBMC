from PyQt5.QtWidgets import QDialog,QVBoxLayout,QListWidgetItem,QListWidget
class KeyListDialog(QDialog):
    def __init__(self, keys, parent=None):
        super(KeyListDialog, self).__init__(parent)

        self.keys = keys
        self.selected_key = None

        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)

        self.listWidget = QListWidget(self)
        for key in self.keys:
            QListWidgetItem(key, self.listWidget)

        self.listWidget.itemClicked.connect(self.onItemClicked)

        self.layout.addWidget(self.listWidget)

        self.setWindowTitle("Select a key")
        self.setGeometry(300, 300, 250, 150)

    def onItemClicked(self, item):
        self.selected_key = item.text()
        self.accept()