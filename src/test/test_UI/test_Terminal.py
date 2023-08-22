'''
这段测试代码主要测试了Terminal类中的`is_valid_file_path`和`is_valid_file_path_with_line`两个方法。首先，需要创建一个 QApplication 实例和 Terminal 实例，然后我们分别进行以下的测试：

- `test_is_valid_file_path`：该测试方法用于测试 Terminal 类的 `is_valid_file_path` 方法。此方法的主要目的是确定给定的文件路径是否有效，例如它是否指向一个存在的文件。在此测试中，我们传入不同的文件路径，并验证方法的返回值是否如我们所期望的那样。

- `test_is_valid_file_path_with_line`：该测试方法用于测试 Terminal 类的 `is_valid_file_path_with_line` 方法。此方法的主要目的是确定给定的字符串是否能被解析为一个有效的文件路径和行号。在此测试中，我们传入不同的字符串，并验证方法的返回值是否如我们所期望的那样。

在每个测试中，我们使用断言函数来验证结果是否符合预期。`assertTrue`和`assertFalse`用于验证一个值是否为`True`或`False`，`assertEquals`用于验证两个值是否相等。如果测试失败，意味着你的方法可能无法正确地处理所有情况，需要对你的实现进行修复或优化。

我们在代码中也创建了一些实例，如`QApplication`和`Terminal`，以模拟实际环境中的使用情况。在运行这些测试之前，我们使用`setUp`方法初始化了所需要的环境和状态。
'''
import unittest
import os 
import sys
root_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root_folder)
from PyQt5.QtGui import QColor, QTextCursor, QTextCharFormat
from ControlFlowGraph.ControlFlowGraphGenerator import Source_Type
from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import QProcess,Qt,QEvent
from UI.MainWindow import MainWindow
from UI.Terminal import Terminal
from loguru import logger
import log_decorator
log_path = "/home/mirage/Visualization-Tool-For-CBMC/src/test/log_UI/log_test_Terminal.log"
logger.add(log_path, rotation="500 MB")  # 每当日志大小超过500MB时，就会创建一个新的日志文件
from log_decorator import log_on_success,count_function,test_class_counts
# 首先我们需要一个Qt应用实例
app = QApplication([])
class TestTerminalMethods(unittest.TestCase):
    @log_on_success
    def setUp(self):
        # 创建一个Terminal实例
        self.terminal = Terminal()
    @log_on_success
    @count_function
    def tearDown(self):
        """ 在每个测试方法后调用。"""
        self.terminal = None
    @log_on_success
    @count_function
    def test_initial_state(self):
        """ 测试 Terminal 是否正确初始化。"""
        self.assertIsNotNone(self.terminal.process)
        self.assertEqual(self.terminal.command_history, [])
        self.assertEqual(self.terminal.command_index, 0)
    @log_on_success
    @count_function
    # 测试单个trace point
    def test_trace_point(self):
         self.terminal.setPlainText("Microsoft Windows [Version 10.0.22621.1992]\n(c) Microsoft Corporation. All rights reserved.\nC:\Windows>tracepoint ATE.c 10")
         QTest.keyClick(self.terminal, Qt.Key_Return)
         self.assertEqual(self.terminal.trace_point_info,[{'ATE.c': '10'}])
         self.assertEqual(self.terminal.command_history,['tracepoint ATE.c 10'])
    @log_on_success
    @count_function
    # 测试多个trace points
    def test_multiple_trace_points(self):
         self.terminal.setPlainText("Microsoft Windows [Version 10.0.22621.1992]\n(c) Microsoft Corporation. All rights reserved.\nC:\Windows>tracepoint ATE.c 10")
         QTest.keyClick(self.terminal, Qt.Key_Return)
         self.terminal.appendPlainText("C:\Windows>tracepoint ATE.c 11")
         QTest.keyClick(self.terminal, Qt.Key_Return)
         self.terminal.appendPlainText("C:\Windows>tracepoint ATE.c 12")
         QTest.keyClick(self.terminal, Qt.Key_Return)
         self.assertEqual(self.terminal.trace_point_info,[{'ATE.c': '10'},{'ATE.c': '11'},{'ATE.c': '12'}])
    @log_on_success
    @count_function
    # 测试清楚多个trace points
    def test_multiple_clear_trace_points(self):
         self.terminal.setPlainText("Microsoft Windows [Version 10.0.22621.1992]\n(c) Microsoft Corporation. All rights reserved.\nC:\Windows>tracepoint ATE.c 10")
         QTest.keyClick(self.terminal, Qt.Key_Return)
         self.terminal.appendPlainText("C:\Windows>tracepoint ATE.c 11")
         QTest.keyClick(self.terminal, Qt.Key_Return)
         self.terminal.appendPlainText("C:\Windows>tracepoint ATE.c 12")
         QTest.keyClick(self.terminal, Qt.Key_Return)
         self.assertEqual(self.terminal.trace_point_info,[{'ATE.c': '10'},{'ATE.c': '11'},{'ATE.c': '12'}])
         self.terminal.clear_tracepoint()
         self.assertEqual(self.terminal.trace_point_info,[])
    @log_on_success
    @count_function
    # 测试clear 命令
    def test_clear(self):
        self.terminal.setPlainText("Microsoft Windows [Version 10.0.22621.1992]\n(c) Microsoft Corporation. All rights reserved.\nC:\Windows>clear")
        QTest.keyClick(self.terminal, Qt.Key_Return)
        self.assertEqual(self.terminal.toPlainText(),"\n")
        self.assertEqual(self.terminal.command_history,['clear'])
    @log_on_success
    @count_function
    # 测试记录的command lines
    def test_command_history(self):
        self.terminal.setPlainText("Microsoft Windows [Version 10.0.22621.1992]\n(c) Microsoft Corporation. All rights reserved.\nC:\Windows>tracepoint ATE.c 10")
        QTest.keyClick(self.terminal, Qt.Key_Return)
        self.terminal.appendPlainText("C:\Windows>clear")
        QTest.keyClick(self.terminal, Qt.Key_Return)
        self.assertEqual(self.terminal.command_history,['tracepoint ATE.c 10', 'clear'])
    @log_on_success
    @count_function
    # 测试查看后面输入的command
    def test_command_trace_forward(self):
        self.terminal.setPlainText("Microsoft Windows [Version 10.0.22621.1992]\n(c) Microsoft Corporation. All rights reserved.\nC:\Windows>tracepoint ATE.c 10")
        QTest.keyClick(self.terminal, Qt.Key_Return)
        self.terminal.appendPlainText("C:\Windows>clear")
        QTest.keyClick(self.terminal, Qt.Key_Return)
        self.assertEqual(self.terminal.command_index,2)
        self.assertEqual(self.terminal.command_history[self.terminal.command_index-1],"clear")
        QTest.keyClick(self.terminal, Qt.Key_Up)
        self.assertEqual(self.terminal.command_index,1)
        self.assertEqual(self.terminal.command_history[self.terminal.command_index-1],"tracepoint ATE.c 10")
    @log_on_success
    @count_function
    # 测试查看前面输入的command
    def test_command_trace_back(self):
        self.terminal.setPlainText("Microsoft Windows [Version 10.0.22621.1992]\n(c) Microsoft Corporation. All rights reserved.\nC:\Windows>tracepoint ATE.c 10")
        QTest.keyClick(self.terminal, Qt.Key_Return)
        self.terminal.appendPlainText("C:\Windows>clear")
        QTest.keyClick(self.terminal, Qt.Key_Return)
        self.assertEqual(self.terminal.command_index,2)
        self.assertEqual(self.terminal.command_history[self.terminal.command_index-1],"clear")
        QTest.keyClick(self.terminal, Qt.Key_Up)
        self.assertEqual(self.terminal.command_index,1)
        self.assertEqual(self.terminal.command_history[self.terminal.command_index-1],"tracepoint ATE.c 10")
        QTest.keyClick(self.terminal, Qt.Key_Down)
        self.assertEqual(self.terminal.command_index,2)
        self.assertEqual(self.terminal.command_history[self.terminal.command_index-1],"clear")

    @log_on_success
    @count_function
    # 测试是否是合法的文件名：比如是file.c或者absoulte path
    def test_is_valid_file_path(self):
        self.assertTrue(self.terminal.is_valid_file_path("/home/mirage/Visualization-Tool-For-CBMC/src/ATE.c"))
        self.assertFalse(self.terminal.is_valid_file_path("/path/to/test.json"))
        self.assertFalse(self.terminal.is_valid_file_path("/path/to/nonexistent_file"))
    @log_on_success
    @count_function
    # 测试当前带有文件名，行序号：file.c, line 8
    def test_is_valid_file_path_with_line(self):
        self.assertEqual(self.terminal.is_valid_file_path_with_line('ATE.c, line 90'),(True, 'ATE.c', 90))
        self.assertEqual(self.terminal.is_valid_file_path_with_line("/home/mirage/Visualization-Tool-For-CBMC/src/file.c, line 5"), (True, "/home/mirage/Visualization-Tool-For-CBMC/src/file.c", 5))
        self.assertEqual(self.terminal.is_valid_file_path_with_line("/home/mirage/Visualization-Tool-For-CBMC/src/file.c"), (True, "/home/mirage/Visualization-Tool-For-CBMC/src/file.c", None))
        self.assertEqual(self.terminal.is_valid_file_path_with_line("/path/to/nonexistent_file, line 5"), False)
        self.assertEqual(self.terminal.is_valid_file_path_with_line("/path/to/nonexistent_file"), False)
    @log_on_success
    @count_function
    # 测试共有的前缀名
    def test_commonprefix(self):
        # 测试案例1：都有相同的前缀
        file_lst_1 = ['test.c', 'test_1.c', 'test_2.c', 'test_3.c']
        self.assertEqual(self.terminal.commonprefix(file_lst_1), "test")

        # 测试案例2：没有相同的前缀
        file_lst_2 = ['test.c', 'demo_1.c', 'file_2.c', 'main_3.c']
        self.assertEqual(self.terminal.commonprefix(file_lst_2), "")

        # 测试案例3：部分有相同的前缀
        file_lst_3 = ['test.c', 'test_1.c', 'demo_2.c', 'main_3.c']
        self.assertEqual(self.terminal.commonprefix(file_lst_3), "")

        # 测试案例4：只有一个文件
        file_lst_4 = ['test.c']
        self.assertEqual(self.terminal.commonprefix(file_lst_4), "test.c")

        # 测试案例5：空的文件列表
        file_lst_5 = []
        self.assertEqual(self.terminal.commonprefix(file_lst_5), "")

        # 测试案例6：所有文件名都完全相同
        file_lst_6 = ['test.c', 'test.c', 'test.c', 'test.c']
        self.assertEqual(self.terminal.commonprefix(file_lst_6), "test.c") 

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])
        
        # 使用TextTestRunner来执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)
    current_file_path = os.path.abspath(__file__)
    with open('/home/mirage/Visualization-Tool-For-CBMC/src/test/test_UI/test_results.txt', 'a') as file:
                file.write(f'{log_decorator.module_test_count}\n')