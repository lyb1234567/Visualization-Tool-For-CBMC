from PyQt5.QtWidgets import QDialog,QVBoxLayout,QListWidgetItem,QListWidget
import copy
class FailureKeyListDialog(QDialog):
    def __init__(self, failure_lst,dict=None,parent=None):
        super(FailureKeyListDialog, self).__init__(parent)

        self.failures = failure_lst 

        self.selected_key = None
        self.selected_keyorder=None

        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)

        self.listWidget = QListWidget(self)
        for i  in range(len(self.failures)):
            QListWidgetItem('Falure'+"_"+str(i), self.listWidget)

        self.listWidget.itemClicked.connect(self.onItemClicked)
        self.layout.addWidget(self.listWidget)

        self.setWindowTitle("Choose a failure case")
        self.setGeometry(300, 300, 250, 150)

    def onItemClicked(self, item):
        self.selected_key = item.text()
        temp=self.selected_key.split('_')
        self.selected_key='status'
        self.selected_keyorder=temp[1]
        self.accept()