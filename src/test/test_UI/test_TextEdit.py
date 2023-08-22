'''
这段代码主要是针对使用 PyQt5 UI 库中的一些自定义功能进行单元测试。

在开头的部分，我们先导入了一些必要的模块，并设置了系统路径以便能找到自定义的 PyQt5 UI 类。这个测试文件包含了三个测试类：TestSearchHighlighter，TestMyHighlighter，和 TestTextEdit。

TestSearchHighlighter 测试类主要用于检查 SearchHighlighter 类的方法。具体来说，我们在 test_highlight_text 方法中测试了 set_highlight_text 方法的效果，验证它是否可以正确地设置要高亮显示的文本。

TestMyHighlighter 测试类针对的是 MyHighlighter 类。在 test_highlight_type 方法中，我们创建了一个 MyHighlighter 实例，然后检查了其高亮格式的下划线样式和颜色是否与预期相符。这个测试帮助保证在指定了源类型为 FAILURE_SOURCE 时，我们的高亮器可以生成正确的高亮格式。

TestTextEdit 测试类测试了 TextEdit 类的功能。在 test_get_line_text 方法中，我们检查 get_line_text 方法是否能正确获取指定行的文本。然后在 test_highlight_line 方法中，我们检查 highlight_line 方法是否能正确设置高亮行号。
'''
import unittest
import os 
import sys
root_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root_folder)
from PyQt5.QtGui import QColor, QTextCursor, QTextCharFormat
from ControlFlowGraph.ControlFlowGraphGenerator import Source_Type
from PyQt5.QtWidgets import QApplication
from UI.TextEdit import MyHighlighter, TextEdit  # 请替换为你的模块名
from UI.MainWindow import MainWindow
app = QApplication([])
window = MainWindow()
from loguru import logger
log_path = "/home/mirage/Visualization-Tool-For-CBMC/src/test/log_UI/log_test_TextEdit.log"
logger.add(log_path, rotation="500 MB")  # 每当日志大小超过500MB时，就会创建一个新的日志文件
from log_decorator import log_on_success,count_function
import log_decorator
class TestMyHighlighter(unittest.TestCase):
    @log_on_success
    @count_function
    def test_highlight_type(self):
        mh = MyHighlighter(SOURCE_TYPE=Source_Type.FAILURE_SOURCE)
        self.assertEqual(mh.highlight_format.underlineStyle(), QTextCharFormat.WaveUnderline)
        self.assertEqual(mh.highlight_format.underlineColor(), QColor("red"))
class TestTextEdit(unittest.TestCase):
    @log_on_success
    @count_function
    def test_get_line_text(self):
        te = TextEdit(editor_window=window)
        te.setPlainText('Line 1\nLine 2\nLine 3')
        self.assertEqual(te.get_line_text(2), 'Line 2')
    @log_on_success
    @count_function
    def test_highlight_line(self):
        text = 'This is a line of text.\nThis is another line of text.'
        te = TextEdit(editor_window=window)
        te.setText(text)
        te.highlight_line(1)
        self.assertEqual(te.highlighter.highlight_line_number, 0)

        te.highlight_line(2)
        self.assertEqual(te.highlighter.highlight_line_number, 1) 


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])
        
        # 使用TextTestRunner来执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)
    current_file_path = os.path.abspath(__file__)
    with open('/home/mirage/Visualization-Tool-For-CBMC/src/test/test_UI/test_results.txt', 'a') as file:
                file.write(f'{log_decorator.module_test_count}\n')
