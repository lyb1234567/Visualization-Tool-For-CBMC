from PyQt5.QtWidgets import QDialog,QVBoxLayout,QListWidgetItem,QListWidget
import copy
class AssertionKeyListDialog(QDialog):
    def __init__(self, assertion_lst,dict=None,parent=None):
        super(AssertionKeyListDialog, self).__init__(parent)

        self.assertion_lst = assertion_lst 

        self.selected_assertion_statement = None
        self.selected_keyorder=None

        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)

        self.listWidget = QListWidget(self)
        for i  in range(len(self.assertion_lst)):
            QListWidgetItem(self.assertion_lst[i], self.listWidget)

        self.listWidget.itemClicked.connect(self.onItemClicked)
        self.layout.addWidget(self.listWidget)

        self.setWindowTitle("Choose a failure case")
        self.setGeometry(300, 300, 250, 150)

    def onItemClicked(self, item):
        self.selected_assertion_statement = item.text()
        self.accept()