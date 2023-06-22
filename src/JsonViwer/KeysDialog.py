from PyQt5.QtWidgets import QDialog,QVBoxLayout,QListWidgetItem,QListWidget
import copy
class KeyListDialog(QDialog):
    def __init__(self, keys,dict=None,parent=None):
        super(KeyListDialog, self).__init__(parent)

        self.keys = keys

        self.selected_key = None
        self.selected_keyorder=None
        self.dict=dict

        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)

        self.listWidget = QListWidget(self)
        temp=copy.deepcopy(self.dict)
        for key in self.keys:
            QListWidgetItem(key+"_"+str(temp[key][0]), self.listWidget)
            temp[key].pop(0)

        self.listWidget.itemClicked.connect(self.onItemClicked)

        self.layout.addWidget(self.listWidget)

        self.setWindowTitle("Select a key")
        self.setGeometry(300, 300, 250, 150)

    def onItemClicked(self, item):
        self.selected_key = item.text()
        temp=self.selected_key.split('_')
        self.selected_key=temp[0]
        self.selected_keyorder=temp[1]
        self.accept()
