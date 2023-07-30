import os
import sys
root_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root_folder)
from PyQt5.QtWidgets import QApplication
from JsonViwer.TreeViewer import TreeViewer
import json 
import unittest
from loguru import logger
app = QApplication([])
tree=TreeViewer()
class TestTreeViewer(unittest.TestCase):
    with open("/home/mirage/Visualization-Tool-For-CBMC/src/test/testjson.json") as f:
        data = json.load(f)
    
    @logger.catch
    def test_initOuterKeyDict(self):
        test_list_1 = ['apple', 'banana', 'cherry', 'banana', 'apple', 'cherry', 'apple', 'banana']
        test_list_2 = ['orange', 'orange', 'orange', 'orange', 'orange']
        test_list_3 = ['apple', 'banana', 'cherry']
        test_list_4 = ['apple', 'banana', 'apple', 'cherry', 'apple', 'cherry', 'banana']
        test_list_5 = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]


        ans_1={"apple":[1,2,3],"banana":[1,2,3],"cherry":[1,2]}
        ans_2 = {'orange': [1,2,3,4,5]}
        ans_3 = {'apple': [1], 'banana': [1], 'cherry': [1]}
        ans_4 = {'apple': [1,2,3], 'banana': [1,2], 'cherry': [1,2]}
        ans_5= {1: [1], 2: [1,2], 3: [1,2,3], 4: [1,2,3,4]}


        # 1
        tree.insertOuterKeys=test_list_1
        tree.initOuterKeyDict()
        self.assertEqual(ans_1,tree.OutKeyDict)
       
        # 2
        tree.insertOuterKeys=test_list_2
        tree.initOuterKeyDict()
        self.assertEqual(ans_2,tree.OutKeyDict)

        # 3
        tree.insertOuterKeys=test_list_3
        tree.initOuterKeyDict()
        self.assertEqual(ans_3,tree.OutKeyDict)

        # 4
        tree.insertOuterKeys=test_list_4
        tree.initOuterKeyDict()
        self.assertEqual(ans_4,tree.OutKeyDict)

        # 5
        tree.insertOuterKeys=test_list_5
        tree.initOuterKeyDict()
        self.assertEqual(ans_5,tree.OutKeyDict)
    @logger.catch
    def test_search(self):
        self.tree_viewer = TreeViewer()
        self.tree_viewer.display(self.data)
        self.tree_viewer.search('name',False)
        self.assertEqual(self.tree_viewer.foundItems[0].text(0), 'name')
        self.assertEqual(self.tree_viewer.foundItems[0].child(0).text(1), 'John')
        self.assertEqual(self.tree_viewer.foundItems[1].text(0), 'name')
        self.assertEqual(self.tree_viewer.foundItems[1].child(0).text(1), 'Mike')

        self.tree_viewer.search('age',False)
        self.assertEqual(self.tree_viewer.foundItems[0].text(0), 'age')
        self.assertEqual(self.tree_viewer.foundItems[0].child(0).text(1),'30')
        self.assertEqual(self.tree_viewer.foundItems[1].text(0), 'age')
        self.assertEqual(self.tree_viewer.foundItems[1].child(0).text(1),'40')

        self.tree_viewer.search('status',False)
        self.assertEqual(self.tree_viewer.foundItems[0].text(0), 'status')
        self.assertEqual(self.tree_viewer.foundItems[0].child(0).text(1),'FAILURE')
        self.assertEqual(self.tree_viewer.foundItems[1].text(0), 'status')
        self.assertEqual(self.tree_viewer.foundItems[1].child(0).text(1),'SUCCESS')

        
           

logger.add("/home/mirage/Visualization-Tool-For-CBMC/src/test/log/Test_JsonTreeViwer.log")
if __name__ == '__main__':
    unittest.main()
        
        