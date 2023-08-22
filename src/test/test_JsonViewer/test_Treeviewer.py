import os
import sys
root_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root_folder)
from PyQt5.QtWidgets import QApplication
from JsonViwer.TreeViewer import TreeViewer
import json 
import unittest
from loguru import logger
from log_decorator import log_on_success,count_function
import log_decorator
app = QApplication([])
log_path = "/home/mirage/Visualization-Tool-For-CBMC/src/test/log_JsonViewer/log_test_Treeviewer.log"
logger.add(log_path, rotation="500 MB")  # 每当日志大小超过500MB时，就会创建一个新的日志文件
class TestTreeViewer(unittest.TestCase):
    @log_on_success
    def setUp(self):
        # Setup function that's called before each test
        self.tree_viewer = TreeViewer()
        with open("/home/mirage/Visualization-Tool-For-CBMC/src/test/test_files/test_json.json") as f:
            self.data = json.load(f)
        self.tree_viewer.display(self.data)
    @log_on_success
    @count_function
    def test_FailureDict(self):
        cnt=1
        for id in self.tree_viewer.FailureDict.keys():
            failure_order=self.tree_viewer.FailureDict[id]
            self.assertEqual(cnt,int(failure_order))
            cnt=cnt+1
    @log_on_success
    @count_function
    def test_viewSourceFile(self):
        # 判断所有Failure Item是否都被存进去了
        self.tree_viewer.search('status',False)
        for item in self.tree_viewer.foundItems:
            if item.child(0).child(0).text(1)=="FAILURE":
                self.assertEqual(id(item.child(0).child(0)) in self.tree_viewer.FailureDict,True)
    @log_on_success
    @count_function
    def test_setFilePath(self):
        test_path = "test_path"
        self.tree_viewer.setFilePath(test_path)
        self.assertEqual(self.tree_viewer.filePath, test_path)
    @log_on_success
    @count_function
    def test_search(self):
        self.tree_viewer.search('name',False)
        self.assertEqual(self.tree_viewer.foundItems[0].text(0), 'name')
        self.assertEqual(self.tree_viewer.foundItems[0].child(0).text(0),'first')
        self.assertEqual(self.tree_viewer.foundItems[0].child(0).child(0).text(1), 'John')



        self.tree_viewer.search('age',False)
        self.assertEqual(self.tree_viewer.foundItems[0].text(0), 'age')
        self.assertEqual(self.tree_viewer.foundItems[0].child(0).text(0),'value')
        self.assertEqual(self.tree_viewer.foundItems[0].child(0).child(0).text(1), '30')

        self.tree_viewer.search('status',False)
        self.assertEqual(self.tree_viewer.foundItems[0].text(0), 'status')
        self.assertEqual(self.tree_viewer.foundItems[0].child(0).text(0),'value')
        self.assertEqual(self.tree_viewer.foundItems[0].child(0).child(0).text(1), 'FAILURE')

        self.tree_viewer.search('name',False)
        self.assertEqual(self.tree_viewer.foundItems[1].text(0), 'name')
        self.assertEqual(self.tree_viewer.foundItems[1].child(0).text(0),'first')
        self.assertEqual(self.tree_viewer.foundItems[1].child(0).child(0).text(1), 'Mike')

        self.tree_viewer.search('age',False)
        self.assertEqual(self.tree_viewer.foundItems[1].text(0), 'age')
        self.assertEqual(self.tree_viewer.foundItems[1].child(0).text(0),'value')
        self.assertEqual(self.tree_viewer.foundItems[1].child(0).child(0).text(1), '40')

        self.tree_viewer.search('status',False)
        self.assertEqual(self.tree_viewer.foundItems[1].text(0), 'status')
        self.assertEqual(self.tree_viewer.foundItems[1].child(0).text(0),'value')
        self.assertEqual(self.tree_viewer.foundItems[1].child(0).child(0).text(1), 'SUCCESS')
    
    @log_on_success
    @count_function
    def test_clear(self):
        # Modify some attributes of treeViewer
        self.tree_viewer.foundItems = ["item1", "item2"]
        self.tree_viewer.FailureDict = {"key": "value"}

        self.tree_viewer.clear()

        # Check that the attributes have been reset
        self.assertEqual(self.tree_viewer.foundItems, [])
        self.assertEqual(self.tree_viewer.FailureDict, {})
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])
        
        # 使用TextTestRunner来执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)
    current_file_path = os.path.abspath(__file__)
    with open('/home/mirage/Visualization-Tool-For-CBMC/src/test/test_JsonViewer/test_results.txt', 'a') as file:
                file.write(f'{log_decorator.module_test_count}\n')
        
        