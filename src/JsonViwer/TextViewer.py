from PyQt5.QtWidgets import QTextEdit
import json
class TextViewer(QTextEdit):
    def __init__(self):
        super().__init__()

    def display(self, json_obj):
        formatted_json = json.dumps(json_obj, indent=4)
        self.setPlainText(formatted_json)