
from PyQt5.QtWidgets import QCheckBox, QVBoxLayout, QDialog, QDialogButtonBox

class MultiFileDialog(QDialog):
    def __init__(self, files, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Select Multiple Files")
        self.layout = QVBoxLayout(self)
        self.checkboxes = []
        for file in files:
            checkbox = QCheckBox(file, self)
            self.layout.addWidget(checkbox)
            self.checkboxes.append(checkbox)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.layout.addWidget(self.buttonBox)

    def getSelectedFiles(self):
        return [cb.text() for cb in self.checkboxes if cb.isChecked()]