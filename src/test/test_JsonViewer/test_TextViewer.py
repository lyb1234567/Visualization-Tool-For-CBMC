import os
import sys
root_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root_folder)
import unittest
from PyQt5.QtWidgets import QApplication
from JsonViwer.TextViewer import TextViewer
import json 
from loguru import logger
from log_decorator import log_on_success,count_function
import log_decorator
app = QApplication([])
log_path = "/home/mirage/Visualization-Tool-For-CBMC/src/test/log_JsonViewer/log_test_TextViewer.log"
logger.add(log_path, rotation="500 MB")  # 每当日志大小超过500MB时，就会创建一个新的日志文件
class TestTextViewer(unittest.TestCase):
    @log_on_success
    def setUp(self):
        self.text_viewer=TextViewer()
        with open("/home/mirage/Visualization-Tool-For-CBMC/src/test/test_files/test_json.json") as f:
            self.data = json.load(f)
    @log_on_success
    @count_function
    def test_display(self):
        expected_output = json.dumps(self.data, indent=4)
        self.text_viewer.display(self.data)
        self.assertEqual(self.text_viewer.toPlainText(),expected_output)

if __name__=="__main__":
    suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])
        
        # 使用TextTestRunner来执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)
    current_file_path = os.path.abspath(__file__)
    with open('/home/mirage/Visualization-Tool-For-CBMC/src/test/test_JsonViewer/test_results.txt', 'a') as file:
                file.write(f'{log_decorator.module_test_count}\n')
        