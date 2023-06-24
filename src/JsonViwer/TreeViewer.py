import os
import sys
root_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_folder)
from PyQt5.QtWidgets import QTreeWidget,QTreeWidgetItem,QMenu,QAction,QDialog
from JsonViwer.FailureKeyDialog import FailureKeyListDialog
class TreeViewer(QTreeWidget):
    def __init__(self):
        super().__init__()
        self.setColumnCount(2)
        self.setHeaderLabels(['Key', 'Value'])
        self.foundItems = []  # List to keep track of found items
        self.currentIndex = 0  # Index to keep track of current selected item
        self.insertOuterKeys=[]
        self.FailureList=[]
        self.SuccessList=[]
    def contextMenuEvent(self, event):
        contextMenu = QMenu(self)

        # Determine the currently clicked item
        currentItem = self.currentItem()

        # Check the text of the current item and adjust the context menu accordingly
        if currentItem.text(0) == 'result':
            failureAction = QAction("View failure", self)
            failureAction.triggered.connect(self.viewFailure)
            contextMenu.addAction(failureAction)
        else:
            nodeAction = QAction("View node", self)
            nodeAction.triggered.connect(self.viewNode)
            contextMenu.addAction(nodeAction)

        # show the context menu
        contextMenu.exec_(event.globalPos())     
    def viewFailure(self):
        seachFailure=True
        failureDialog=FailureKeyListDialog(self.FailureList)
        result = failureDialog.exec_()
        if result == QDialog.Accepted:
            query=failureDialog.selected_key
            order=int(failureDialog.selected_keyorder)
            self.search(query,seachFailure,order)

    def viewNode(self):
        pass
    def search(self, query,searchFailure,order=None):
        found=False
        if not self.foundItems or self.foundItems[0].text(0) != query:
            # Clear previous search results if new search query
            self.foundItems.clear()
            self._search(query, self.invisibleRootItem(),searchFailure)

        if self.foundItems:
            # If matches are found, select the current item
            if order:
                self.setCurrentItem(self.foundItems[order])
            else:
                self.setCurrentItem(self.foundItems[0])
            found=True
        else:
            # If no matches found, clear the selection
            self.setCurrentItem(None)
        return found

    def _search(self, query, item,ifFailure=False):
        for i in range(item.childCount()):
            child = item.child(i)
            key = child.text(0)
            if query == key and not ifFailure:
                self.foundItems.append(child)
                child.setExpanded(True)
            elif query==key and ifFailure:
                if child.child(0).text(1)=="FAILURE":
                    parent=child.parent()
                    for i  in range(parent.childCount()):
                        sibling=parent.child(i)
                        if sibling.text(0)=="description":
                            sibling.setExpanded(True)
                    self.foundItems.append(child)
                    child.setExpanded(True)
            self._search(query, child,ifFailure)  # Recursive call for child items
    def display(self, json_obj, root_item=None):
        if root_item is None:
            if isinstance(json_obj, list):
                for element in json_obj:
                    if isinstance(element, dict):
                       for key in element.keys():
                           self.insertOuterKeys.append(key)
                self.initOuterKeyDict()
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
            if json_obj=="FAILURE":
                if not self.FailureList:
                        self.FailureList.append(1)
                else:
                        temp=self.FailureList[-1]+1
                        self.FailureList.append(temp)
            child = QTreeWidgetItem()
            child.setText(1, str(json_obj))
            root_item.addChild(child)
    #  set order for each key in the outer key lists

    def initOuterKeyDict(self):
        self.OutKeyDict={}
        if self.insertOuterKeys:
            for key in self.insertOuterKeys:
                self.OutKeyDict[key]=[]
            for key in self.insertOuterKeys:
                if not self.OutKeyDict[key]:
                    self.OutKeyDict[key].append(1)
                else:
                    temp=self.OutKeyDict[key][-1]+1
                    self.OutKeyDict[key].append(temp)
            