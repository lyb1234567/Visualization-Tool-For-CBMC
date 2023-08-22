import os
import sys
root_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root_folder)
from PyQt5.QtWidgets import QApplication,QDialog
from JsonViwer.FailureKeyDialog import AssertionKeyListDialog
import unittest
from loguru import logger
from log_decorator import log_on_success,count_function
import log_decorator
app = QApplication([])
log_path = "/home/mirage/Visualization-Tool-For-CBMC/src/test/log_JsonViewer/log_test_AssertionListKeyDialog.log"
logger.add(log_path, rotation="500 MB")  # 每当日志大小超过500MB时，就会创建一个新的日志文件
class TestAssertionDialogKeyList(unittest.TestCase):
    @count_function
    def setUp(self):
        self.assertions = ['assert1', 'assert2', 'assert3']
        self.dialog = AssertionKeyListDialog(self.assertions)
    @log_on_success
    @count_function
    def test_populate(self):
        # 1. 验证list widget是否正确填充
        self.assertEqual(self.dialog.listWidget.count(),len(self.assertions))
    @log_on_success
    @count_function
    def simulate_click(self):
        self.dialog.listWidget.setCurrentRow(1)  # 设置第二项为当前选择
        self.dialog.onItemClicked(self.dialog.listWidget.currentItem())
        self.assertEqual(self.dialog.selected_assertion_statement,"assert2")
        self.assertEqual(self.dialog.result,QDialog.Accepted)

        self.dialog.listWidget.setCurrentRow(0)  # 设置第一项为当前选择
        self.dialog.onItemClicked(self.dialog.listWidget.currentItem())
        self.assertEqual(self.dialog.selected_assertion_statement,"assert1")
        self.assertEqual(self.dialog.result,QDialog.Accepted)


        self.dialog.listWidget.setCurrentRow(2)  # 设置第三项为当前选择
        self.dialog.onItemClicked(self.dialog.listWidget.currentItem())
        self.assertEqual(self.dialog.selected_assertion_statement,"assert2")
        self.assertEqual(self.dialog.result,QDialog.Accepted)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])
        
        # 使用TextTestRunner来执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)
    current_file_path = os.path.abspath(__file__)
    with open('/home/mirage/Visualization-Tool-For-CBMC/src/test/test_JsonViewer/test_results.txt', 'a') as file:
                file.write(f'{log_decorator.module_test_count}\n')
        