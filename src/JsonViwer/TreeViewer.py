import typing
from PyQt5.QtWidgets import QTreeWidget,QTreeWidgetItem
class TreeViewer(QTreeWidget):
    def __init__(self):
        super().__init__()
        self.setColumnCount(2)
        self.setHeaderLabels(['Key', 'Value'])
        self.foundItems = []  # List to keep track of found items
        self.currentIndex = 0  # Index to keep track of current selected item
        self.insertOuterKeys=[]
    def search(self, query):
        if not self.foundItems or self.foundItems[0].text(0) != query:
            # Clear previous search results if new search query
            self.foundItems.clear()
            self.currentIndex = 0
            self._search(query, self.invisibleRootItem())

        if self.foundItems:
            # If matches are found, select the current item
            self.setCurrentItem(self.foundItems[self.currentIndex])
            self.currentIndex = (self.currentIndex + 1) % len(self.foundItems)
        else:
            # If no matches found, clear the selection
            self.setCurrentItem(None)

    def _search(self, query, item):
        for i in range(item.childCount()):
            child = item.child(i)
            key = child.text(0)
            if query == key:
                self.foundItems.append(child)
                child.setExpanded(True)
            self._search(query, child)  # Recursive call for child items
    def display(self, json_obj, root_item=None):
        if root_item is None:
            if isinstance(json_obj, list):
                for element in json_obj:
                    if isinstance(element, dict):
                       for key in element.keys():
                           self.insertOuterKeys.append(key)
                root_item = QTreeWidgetItem(self)
                root_item.setText(0, f'Array[{len(json_obj)}]')
            else:
                root_item = self.invisibleRootItem()

        if isinstance(json_obj, dict):
            for key in json_obj:
                child = QTreeWidgetItem()
                child.setText(0, str(key))
                root_item.addChild(child)
                self.display(json_obj[key], child)
        elif isinstance(json_obj, list):
            for i, value in enumerate(json_obj):
                child = QTreeWidgetItem()
                child.setText(0, str(i))
                root_item.addChild(child)
                self.display(value, child)
        else:
            child = QTreeWidgetItem()
            child.setText(1, str(json_obj))
            root_item.addChild(child)