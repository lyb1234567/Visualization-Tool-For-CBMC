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
from UI.TextEdit import SearchHighlighter, MyHighlighter, TextEdit  # 请替换为你的模块名
from UI.MainWindow import MainWindow
from UI.Terminal import Terminal

# 首先我们需要一个Qt应用实例
app = QApplication([])

class TestTerminalMethods(unittest.TestCase):
    def setUp(self):
        # 创建一个Terminal实例
        self.terminal = Terminal()

    def test_is_valid_file_path(self):
        self.assertTrue(self.terminal.is_valid_file_path("/path/to/test.c"))
        self.assertTrue(self.terminal.is_valid_file_path("/path/to/test.json"))
        self.assertFalse(self.terminal.is_valid_file_path("/path/to/nonexistent_file"))

    def test_is_valid_file_path_with_line(self):
        self.assertEqual(self.terminal.is_valid_file_path_with_line("/home/mirage/Visualization-Tool-For-CBMC/src/test_trace_1.json, line 5"), (True, "/home/mirage/Visualization-Tool-For-CBMC/src/test_trace_1.json", 5))
        self.assertEqual(self.terminal.is_valid_file_path_with_line("/home/mirage/Visualization-Tool-For-CBMC/src/test_trace_1.json"), (True, "/home/mirage/Visualization-Tool-For-CBMC/src/test_trace_1.json", None))
        self.assertEqual(self.terminal.is_valid_file_path_with_line("/path/to/nonexistent_file, line 5"), False)
        self.assertEqual(self.terminal.is_valid_file_path_with_line("/path/to/nonexistent_file"), False)

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
    unittest.main()