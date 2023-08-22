import os
import sys
import unittest
from loguru import logger
root_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root_folder)
from UI.utils import extract_variables,extract_file_name,extract_file_name_without_extension,extract_command
log_path = "/home/mirage/Visualization-Tool-For-CBMC/src/test/log_UI/log_test_utils.log"
logger.add(log_path, rotation="500 MB")  # 每当日志大小超过500MB时，就会创建一个新的日志文件
from log_decorator import log_on_success,count_function
import log_decorator
class TestUtils(unittest.TestCase):
    @log_on_success
    @count_function
    def test_extract_variables(self):
            self.assertEqual(set(extract_variables("assertion x <= y")), set(['x', 'y']))
            self.assertEqual(set(extract_variables("assertion a > b")), set(['a', 'b']))
            self.assertEqual(set(extract_variables("assertion z / x + asdas <= y")), set(['z', 'x', 'asdas', 'y']))
            self.assertEqual(set(extract_variables("assertion p == q")), set(['p', 'q']))
            self.assertEqual(set(extract_variables("assertion x + x < y")), set(['x', 'y']))
            self.assertEqual(set(extract_variables("assertion var_name <= y")), set(['var_name', 'y']))
            self.assertEqual(set(extract_variables("assertion x < x")), set(['x']))
            self.assertEqual(set(extract_variables("assertion x / (y + z) <= a")), set(['x', 'y', 'z', 'a']))
            self.assertEqual(set(extract_variables("assertion *value")), set(['value']))
            self.assertEqual(set(extract_variables("assertion array[i] > 0 && array[j] < 0")), set(['i', 'j']))
            self.assertEqual(set(extract_variables("assertion size > 0")), set(['size']))
            self.assertEqual(set(extract_variables("assertion value != NULL")), set(['value']))
            self.assertEqual(set(extract_variables("assertion value != 3")), set(['value']))
            self.assertEqual(set(extract_variables("assertion array[i+1] == 0")), set(['i']))
            self.assertEqual(set(extract_variables("assertion array[i] > 0 && array[j] < 0 || array [k] < 3  ")), set(['i','j','k']))
            self.assertEqual(set(extract_variables("assertion array[i] > 0 && array[j] < 0 || array [k] < 3 && array[u] < 4  ")), set(['i','j','k','u']))
            self.assertEqual(set(extract_variables("assertion array[i] > 0 && array[j-4] < 0 || array [k+1] < 3  ")), set(['i','j','k']))
    @log_on_success
    @count_function
    def test_extract_file(self):
        self.assertEqual(extract_file_name("/home/mirage/Visualization-Tool-For-CBMC/src/test/test_Terminal.py"),"test_Terminal.py")
        self.assertEqual(extract_file_name("/home/mirage/Visualization-Tool-For-CBMC/src/test/test_1.py"),"test_1.py")    
        self.assertEqual(extract_file_name("/home/mirage/Visualization-Tool-For-CBMC/src/test/test_2.py"),"test_2.py") 
    @log_on_success
    @count_function
    def test_extract_file(self):
        self.assertEqual(extract_file_name_without_extension("/home/mirage/Visualization-Tool-For-CBMC/src/test/test_Terminal.py"),"test_Terminal")
        self.assertEqual(extract_file_name_without_extension("/home/mirage/Visualization-Tool-For-CBMC/src/test/test_1.py"),"test_1")    
        self.assertEqual(extract_file_name_without_extension("/home/mirage/Visualization-Tool-For-CBMC/src/test/test_2.py"),"test_2")

    @log_on_success
    @count_function
    def test_extract_command(self):
        self.assertEqual(extract_command("xxx>clear"),"clear")
        self.assertEqual(extract_command("xxx>help"),"help")
        self.assertEqual(extract_command("xxx>tracepoint file.c 10"),"tracepoint file.c 10")
        self.assertEqual(extract_command("xxx>run file.c "),"run file.c")   
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])
        
        # 使用TextTestRunner来执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)
    current_file_path = os.path.abspath(__file__)
    with open('/home/mirage/Visualization-Tool-For-CBMC/src/test/test_UI/test_results.txt', 'a') as file:
        file.write(f'{log_decorator.module_test_count}\n')
    
    