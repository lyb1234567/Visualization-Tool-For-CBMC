'''
TODO
1. Visualization of trace trees
2. user should be able to see the counterexamples by hovering around the highlighted code
'''
from graphviz import Digraph
import os
import sys
import json
root_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_folder)
from PyQt5.QtWidgets import QTreeWidget,QTreeWidgetItem,QMenu,QAction,QDialog,QGraphicsScene,QGraphicsView
from PyQt5.QtCore import Qt
from JsonViwer.FailureKeyDialog import AssertionKeyListDialog
from UI.utils import extract_file_name_without_extension,extract_variables,is_trace_file
from ControlFlowGraph.ControlFlowGraphGenerator import Source_Type
from GraphViewer.NodeItem import Node
from GraphViewer.ArrowItem import Arrow
class MyGraphicsView(QGraphicsView):
    def __init__(self, scene,editor_window=None):
        self.editor_window=editor_window
        super().__init__(scene)
    def closeEvent(self, event):
        self.editor_window.terminal.clear_tracepoint()
        # 在这里做你想做的事
        event.accept()  # 确认关闭事件
class TreeViewer(QTreeWidget):
    def __init__(self,editor_window=None,json_window=None,filePath=None,cfg=None,trace_num=None,run_by_editor=False):
        super().__init__()
        self.setColumnCount(2)
        self.setHeaderLabels(['Key', 'Value'])
        self.filePath=filePath
        self.foundItems = []  # List to keep track of found items
        self.currentIndex = 0  # Index to keep track of current selected item
        self.insertOuterKeys=[]
        self.FailureList=[]
        self.SuccessList=[]
        self.FailureSourceList=[]
        self.FailureReasonDict={}
        self.FailureReasonList=[]
        self.variableDict={}
        self.FailureDict={}
        self.assertion_lst=[]
        self.editor_window=editor_window
        self.json_window=json_window
        self.trace_num=0
        self.cfg=cfg
        self.graphicView=None
        self.run_by_editor=run_by_editor
        # 这个变量是用来传递trace name的，在用户想要看trace的时候
        self.trace_view_num=trace_num
        self.counterNum=0
        self.counterexamplesSourceDict={}
        self.trace_files=[]
    def setFilePath(self,filePath):
        self.filePath=filePath
    def clear(self):
        super().clear()
        self.foundItems.clear()  # Clear foundItems list
        self.FailureDict.clear()
        self.FailureSourceList.clear()
        self.variableDict.clear()
        self.FailureList.clear()
        self.insertOuterKeys.clear()
        self.SuccessList.clear()
        self.trace_num=0
        self.FailureReasonDict.clear()
        self.FailureReasonList.clear()
        self.counterexamplesSourceDict.clear()
        self.counterNum=0
        self.trace_files.clear()
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # You can get the item under the cursor with the itemAt method
            item = self.itemAt(event.pos())
            if item:
                if item.text(1):
                    if item.text(1)=="FAILURE":
                        pass
                # Do something with the item...TODO
        super().mousePressEvent(event)
    def contextMenuEvent(self, event):
        contextMenu = QMenu(self)
        # Determine the currently clicked item
        currentItem = self.itemAt(event.pos())
        if not currentItem:
            pass
        # Check the text of the current item and adjust the context menu accordingly
        if currentItem.text(0) and self.run_by_editor:
            if currentItem.text(0) == 'result':
                failureAction = QAction("View failure", self)
                failureAction.triggered.connect(self.viewAssertion)
                contextMenu.addAction(failureAction)
        else:
            if currentItem.text(1) and self.run_by_editor:
                if currentItem.text(1) == 'FAILURE':
                    filename=self.getSourceFile(id(currentItem))['file']
                    linenumber=self.getSourceFile(id(currentItem))['line']
                    trace_file=self.trace_files[self.FailureDict[id(currentItem)]-1]
                    trace_num=self.FailureDict[id(currentItem)]
                    nodeAction = QAction("View Source File", self)
                    nodeAction.triggered.connect(lambda: self.viewSourceFile(filename,linenumber,SOURCE_TYPE=Source_Type.FAILURE_SOURCE,cfg=self.cfg,trace_num=trace_num))
                    contextMenu.addAction(nodeAction)
                    parent=currentItem.parent().parent()
                    assertion_statement=None
                    for i in range(parent.childCount()):
                        sibling=parent.child(i)
                        if sibling.text(0)=="description":
                            assertion_statement=sibling.child(0).text(1)
                    if assertion_statement!=None:
                        printTraceAction = QAction("View traces", self)
                        printTraceAction.triggered.connect(lambda: self.print_traces_graph(assertion_statement,trace_num=trace_num))
                        contextMenu.addAction(printTraceAction)              
        # show the context menu
        contextMenu.exec_(event.globalPos())
    # 获取某个特定assertion_statement，对应的break point trace 信息
    # break point的列表信息可能如下[{'file2.c':12},{'file2.c':13}]
    def get_trace_point_info(self,assertion_statement):
        res=""
        for file_line_dict in self.editor_window.terminal.trace_point_info:
            for file_name,line_number in file_line_dict.items():
                temp_info=self.cfg.get_assertion_info(fileName=file_name,line_number=int(line_number),assertion_statement=assertion_statement)
                if temp_info:
                    temp_res="at {0}, line {1}".format(file_name,line_number)+"\n"+'\t'+temp_info+'\n'
                else:
                    temp_res="at {0}, line {1}".format(file_name,line_number)+"\n"+'\t'+"There is no specific trace information"+'\n'
                res=res+temp_res
        return res
    def print_traces_graph(self,assertion_statement,trace_num=None):
        self.editor_window.terminal.cur_assertion_statement=assertion_statement
        self.editor_window.terminal.cfg=self.cfg
        self.editor_window.terminal.appendPlainText(self.get_trace_point_info(assertion_statement))
        self.editor_window.terminal.process.write(b'\n')
        assertion_trace=self.cfg.assertion_trace_total[assertion_statement]
        y = 0
        prev_node = None
        scene = QGraphicsScene()
        for statement in assertion_trace:
            if isinstance(statement,dict):
                for key in statement.keys():
                    node = Node(text=key,cfg=self.cfg,trace_num=trace_num,tree_viewer=self)
                    node.node_info.update(statement[key])
                    node.node_info.update({'assertion_statement':assertion_statement})
                node.setPos(0, y)
                y += 100  # Adjust this value to change the vertical spacing between nodes
                scene.addItem(node)
                if prev_node is not None:
                    arrow = Arrow(prev_node, node)
                    scene.addItem(arrow)
                prev_node = node
            else:
                node = Node(text=statement,cfg=self.cfg,trace_num=trace_num,tree_viewer=self)
                node.setPos(0, y)
                y += 100  # Adjust this value to change the vertical spacing between nodes
                scene.addItem(node)
                if prev_node is not None:
                    arrow = Arrow(prev_node, node)
                    scene.addItem(arrow)
                prev_node = node
        self.graphicView = MyGraphicsView(scene,editor_window=self.editor_window)
        self.graphicView.resize(800, 600)
        self.graphicView.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.graphicView.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.graphicView.show()
    def viewAssertion(self):
        seachFailure=True
        failureDialog=AssertionKeyListDialog(self.assertion_lst)
        result = failureDialog.exec_()
        if result == QDialog.Accepted:
            selected_assertion_statement=failureDialog.selected_assertion_statement
            self.search(selected_assertion_statement,seachFailure)
    def viewSourceFile(self,filename,linenumber,SOURCE_TYPE=None,cfg=None,trace_num=None,assertion_statement=None):
        #  viewer sourcefile TODO
        self.editor_window.openFile(filename,linenumber,SOURCE_TYPE,cfg=cfg,assertion_statement=assertion_statement)
    def getSourceFile(self,Failure_id):
        #  viewer sourcefile TODO
         Failure_index= self.FailureDict[Failure_id]
         Sourcedict=self.FailureSourceList[Failure_index-1]
         return Sourcedict
    def search(self, query,searchFailure,searchCounterExamples=False,order=None):
        found=False
        if not self.foundItems or self.foundItems[0].text(0) != query:
            # Clear previous search results if new search query
            self.foundItems.clear()
            self._search(query, self.invisibleRootItem(),searchFailure,searchCounterExamples)

        if self.foundItems:
            # If matches are found, select the current item
            if order is not None :
                self.setCurrentItem(self.foundItems[order])
            else:
                for i in range(len(self.foundItems)):
                    self.setCurrentItem(self.foundItems[i])
            found=True
        else:
            # If no matches found, clear the selection
            self.setCurrentItem(None)
        return found

    def _search(self, query, item,ifFailure=False,ifCounterExample=False):
        for i in range(item.childCount()):
            child = item.child(i)
            key = child.text(0)
            if query == key and not ifFailure and not ifCounterExample:
                self.foundItems.append(child)
                child.setExpanded(True)
            elif key=="description" and child.child(0).text(1)==query:
                 parent=child.parent()
                 parent.setExpanded(True)
                 for i  in range(parent.childCount()):
                    sibling=parent.child(i)
                    if sibling.text(0)=="description":
                        sibling.setExpanded(True)
                    if sibling.text(0)=='status':
                        sibling.setExpanded(True)
            elif query==key and ifFailure and not ifCounterExample:
                if child.child(0).text(1)=="FAILURE":
                    parent=child.parent()
                    parent.setExpanded(True)
                    for i  in range(parent.childCount()):
                        sibling=parent.child(i)
                        if sibling.text(0)=="description":
                            sibling.setExpanded(True)
                        if sibling.text(0)=="sourceLocation":
                            source_dict={}
                            for j in range(sibling.childCount()):
                                sibling_child=sibling.child(j)
                                source_dict[sibling_child.text(0)]=sibling_child.child(0).text(1)
                            self.FailureSourceList.append(source_dict)
                    self.foundItems.append(child)
                    child.setExpanded(True)
            self._search(query, child,ifFailure,ifCounterExample)  # Recursive call for child items
            
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
                if key == "trace":  # If the key is "trace", write the object to a JSON file
                    self.trace_num=self.trace_num+1
                    file_name = os.path.join(os.getcwd(), f"{extract_file_name_without_extension(self.json_window.filePath)}_trace_{self.trace_num}.json")
                    with open(file_name, 'w') as f:
                            json.dump(json_obj[key], f, indent=4)
                    self.trace_files.append(file_name)
                if key=="description":
                    if json_obj.get('status') !=None:
                            self.counterNum=self.counterNum+1
                            assertion_statement=json_obj[key]
                            self.assertion_lst.append(assertion_statement)
                if key=="reason":
                    if not self.FailureReasonList:
                        self.FailureReasonList.append(1)
                        self.FailureReasonDict[id(child)]=1
                    else:
                        temp=self.FailureReasonList[-1]+1
                        self.FailureReasonDict[id(child)]=temp
                        self.FailureReasonList.append(temp)
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
            if json_obj=="FAILURE":
                if not self.FailureList:
                        self.FailureDict[id(child)]=1
                        self.FailureList.append(1)
                else:
                        temp=self.FailureList[-1]+1
                        self.FailureDict[id(child)]=temp
                        self.FailureList.append(temp)
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
    def ExpandAllFailure(self):
        self.search("status",True)
        