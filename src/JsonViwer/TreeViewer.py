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
from PyQt5.QtWidgets import QTreeWidget,QTreeWidgetItem,QMenu,QAction,QDialog
from PyQt5.QtCore import Qt
from JsonViwer.FailureKeyDialog import FailureKeyListDialog
from JsonViwer.TextfileViewer import TextFileViewer
from UI.utils import extract_file_name_without_extension,extract_variables,is_trace_file
from ControlFlowGraph.ControlFlowGraphGenerator import ControlGraphGenerator, Source_Type
class TreeViewer(QTreeWidget):
    def __init__(self,editor_window=None,json_window=None,filePath=None,cfg=None,trace_num=None):
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
        self.counterexamplesvariable={}
        self.editor_window=editor_window
        self.json_window=json_window
        self.trace_num=0
        self.cfg=cfg
        # 这个变量是用来传递trace name的，在用户想要看trace的时候
        self.trace_view_num=trace_num
        self.counterNum=0
        self.counterexamplesSourceDict={}
        self.trace_files=[]
        with open('counterexamplerecord.txt', 'w') as f:
                pass  # Writing nothing to the file effectively clears it
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
        self.counterexamplesvariable.clear()
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
        if currentItem.text(0):
            if currentItem.text(0) == 'result':
                failureAction = QAction("View failure", self)
                failureAction.triggered.connect(self.viewFailure)
                contextMenu.addAction(failureAction)
        else:
            if currentItem.text(1):
                if currentItem.text(1) == 'FAILURE':
                    filename=self.getSourceFile(id(currentItem))['file']
                    linenumber=self.getSourceFile(id(currentItem))['line']
                    trace_file=self.trace_files[self.FailureDict[id(currentItem)]-1]
                    trace_num=self.FailureDict[id(currentItem)]
                    nodeAction = QAction("View Source File", self)
                    nodeAction.triggered.connect(lambda: self.viewSourceFile(filename,linenumber,SOURCE_TYPE=Source_Type.FAILURE_SOURCE,cfg=self.cfg,trace_num=trace_num))
                    contextMenu.addAction(nodeAction)
                    viewTraceAction = QAction("View Trace", self)
                    viewTraceAction.triggered.connect(lambda: self.viewtraces(pass_trace_file=trace_file,cfg=self.cfg,trace_num=trace_num))
                    contextMenu.addAction(viewTraceAction)
                    parent=currentItem.parent().parent()
                    assertion_statement=None
                    for i in range(parent.childCount()):
                        sibling=parent.child(i)
                        if sibling.text(0)=="description":
                            assertion_statement=sibling.child(0).text(1)
                    if assertion_statement!=None:
                        printTraceAction = QAction("print traces", self)
                        printTraceAction.triggered.connect(lambda: self.print_traces(assertion_statement))
                        contextMenu.addAction(printTraceAction)
                if currentItem.parent().text(0)=="lhs":
                    # TODO:右键点击lhs可以返回到对应的文件代码行中
                    navigate_file_name=None
                    naviagte_line_number=None
                    parent_parent=currentItem.parent().parent()
                    for i in range(parent_parent.childCount()):
                        sibling=parent_parent.child(i)
                        if sibling.text(0)=="sourceLocation":
                            for j in range(sibling.childCount()):
                                            sibling_child=sibling.child(j)
                                            if sibling_child.text(0)=="file":
                                                navigate_file_name=sibling_child.child(0).text(1)
                                            if sibling_child.text(0)=="line":
                                                naviagte_line_number=sibling_child.child(0).text(1)
                    nodeAction = QAction("View Source File", self)
                    nodeAction.triggered.connect(lambda: self.viewSourceFile(navigate_file_name,naviagte_line_number,SOURCE_TYPE=Source_Type.TRACE_SOURCE,cfg=self.cfg,trace_num=self.trace_view_num))
                    contextMenu.addAction(nodeAction)
                    
                                            
                
                    
        # show the context menu
        contextMenu.exec_(event.globalPos())     
    def print_traces(self,assertion_statement):
        import time
        dot = Digraph(comment='Assertion Tracing')
        assertion_trace=self.cfg.assertion_trace_total[assertion_statement]
        for idx, step in enumerate(assertion_trace):
                # Adding the index to the node name to differentiate nodes with the same value
                dot.node(f'{step}_{idx}', label=step, shape='box', style='rounded', width='2', height='1')

                # Don't try to add an edge for the first item in the list
                if idx > 0:
                    dot.edge(f'{assertion_trace[idx-1]}_{idx-1}', f'{step}_{idx}')
        dot.render('Trace_graph/assertion_trace.gv', view=False)
    def viewFailure(self):
        seachFailure=True
        failureDialog=FailureKeyListDialog(self.FailureList)
        result = failureDialog.exec_()
        if result == QDialog.Accepted:
            query=failureDialog.selected_key
            order=int(failureDialog.selected_keyorder)
            self.search(query,seachFailure,order)
    def viewtraces(self,pass_trace_file=None,cfg=None,trace_num=None):
        if is_trace_file(self.filePath):
            self.ExpandAllCounterExamples()
        elif pass_trace_file:
            from JsonViwer.MainJsonWindow import MainWindow as JsonWindow
            trace_json_window=JsonWindow(filePath=pass_trace_file,editor_window=self.editor_window,cfg=cfg,trace_num=trace_num)
            trace_json_window.treeViewer.ExpandAllCounterExamples()
            trace_json_window.show()
    def viewSourceFile(self,filename,linenumber,SOURCE_TYPE=None,cfg=None,trace_num=None):
        #  viewer sourcefile TODO
        self.editor_window.openFile(filename,linenumber,SOURCE_TYPE,cfg=cfg,trace_num=trace_num)
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
            elif query==key and ifFailure and ifCounterExample:
                child.parent().parent().setExpanded(True)
                child.parent().setExpanded(True)
                child.setExpanded(True)
                if child.text(0)=="lhs":
                    for key in self.counterexamplesvariable.keys():
                        sameFile=False
                        hidden=False
                        value_lst=self.counterexamplesvariable[key]
                        fileName=self.FailureSourceList[key-1]['file']
                        for value in value_lst:
                            if child.child(0).text(1)==value:
                                parent=child.parent()
                                for i  in range(parent.childCount()):
                                    sibling=parent.child(i)
                                    if sibling.text(0)=="sourceLocation":
                                        for j in range(sibling.childCount()):
                                            sibling_child=sibling.child(j)
                                            if sibling_child.text(0)=="file" and sibling_child.child(0).text(1)==fileName:
                                                sameFile=True
                                    if sibling.text(0)=="hidden":
                                       if sibling.child(0).text(1)=='False':
                                           hidden=False
                                       else:
                                           hidden=True
                                    if sibling.text(0)=="value":
                                        sibling.setExpanded(True)
                                        for j in range(sibling.childCount()):
                                            sibling_child=sibling.child(j)
                                            if sibling_child.text(0)=="data" and sameFile and not hidden :
                                                with open('counterexamplerecord.txt',"a") as f:
                                                    f.write(fileName+'\n')
                                                    f.write(value+'\n')
                                                    f.write(sibling_child.child(0).text(1))
                                                    f.write('\n\n')
                
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
                        if json_obj.get('status')=='FAILURE':
                            self.counterNum=self.counterNum+1
                            assertion_statement=json_obj[key]
                            self.counterexamplesvariable[self.counterNum]=extract_variables(assertion_statement)
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
    def ExpandAllCounterExamples(self):
        self.search("lhs",True,True)
        self.search("value",True,True)
        self.search("data",True,True)
    def generate_counterexamples_source(self):
        with open('counterexamplerecord.txt', 'r') as f:
            # Split the file contents into groups
            groups = f.read().split('\n\n')

            # Process each group
            for group in groups:
                # Split the group into lines
                lines = group.split('\n')

                if(len(lines)!=3):
                    break
                # Get the filename, variable, and counterexample
                filename, variable, counterexample = lines[0],lines[1],lines[2]

                # Convert counterexample to integer
                counterexample = int(counterexample)

                # If the filename is not yet in the data, add it with an empty dictionary as its value
                if filename not in self.counterexamplesSourceDict:
                    self.counterexamplesSourceDict[filename] = {}

                # If the variable is not yet in the filename's dictionary, add it with an empty list as its value
                if variable not in self.counterexamplesSourceDict[filename]:
                    self.counterexamplesSourceDict[filename][variable] = set()
                # Append the counterexample to the variable's list
                self.counterexamplesSourceDict[filename][variable].add(counterexample)
        