'''
这是一个用于测试文本搜索和高亮显示功能的单元测试模块。这个模块中包含了两个测试类，TestSearchDialog_1 和 TestSearchDialog_2。每个类中都有一个setUp方法和一个测试方法。

在setUp方法中，我们首先创建一个 QApplication 实例，然后创建一个 MainWindow 实例，并将其编辑器设置为自定义的 TextEdit 实例。我们在编辑器中设置了一些文本用于测试，并将编辑器添加到 MainWindow 的标签页中。然后，我们创建一个 SearchDialog 实例，并将 MainWindow 实例传递给它。

在 test_perform_search 方法中，我们首先设置搜索框的文本，然后执行搜索。我们断言返回的匹配数量，当前的匹配项，和匹配标签的文本是否符合预期。我们还测试了向前和向后搜索的功能。

TestSearchDialog_1 中的测试文本是 'This is a sample text for testing. Testing is important.'，并且我们在搜索框中设置的文本是 'is'。

TestSearchDialog_2 中的测试文本是 'Hello\n Hello\n Hello\n'，并且我们在搜索框中设置的文本是 'He'。

在这个模块的最后，我们调用 unittest.main() 方法来运行测试。
'''

import unittest
import os
import sys
root_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root_folder)
from UI.TextEdit import SearchHighlighter, MyHighlighter, TextEdit  # 请替换为你的模块名
from UI.MainWindow import MainWindow
from UI.SearchDialog import SearchDialog
from PyQt5.QtWidgets import QApplication
class TestSearchDialog_1(unittest.TestCase):
    def setUp(self):
        self.app = QApplication(sys.argv)
        self.main_win = MainWindow()
        self.main_win.editor = TextEdit(editor_window=self.main_win)
        self.main_win.editor.setText('This is a sample text for testing. Testing is important.')
        self.main_win.tabWidget.addTab(self.main_win.editor, "test")
        self.dialog = SearchDialog(self.main_win)

    def test_perform_search(self):
        self.dialog.search_box.setText('is')
        self.dialog.perform_search()
        self.assertEqual(len(self.dialog.matches), 3)  # "is" appears twice
        self.assertEqual(self.dialog.current_match, 0)  # current match is the first one
        self.assertEqual(self.dialog.match_label.text(), '1 of 3')  # label text is correct
        self.dialog.perform_search_next()
        self.assertEqual(self.dialog.current_match, 1)

        self.dialog.perform_search_previous()
        self.assertEqual(self.dialog.current_match, 0)

        self.dialog.perform_search_previous()
        self.assertEqual(self.dialog.current_match, 2)
        
        self.dialog.perform_search_next()
        self.assertEqual(self.dialog.current_match, 0)

        self.dialog.perform_search_next()
        self.assertEqual(self.dialog.current_match, 1)

    
class TestSearchDialog_2(unittest.TestCase):
    def setUp(self):
        self.app = QApplication(sys.argv)
        self.main_win = MainWindow()
        self.main_win.editor = TextEdit(editor_window=self.main_win)
        self.main_win.editor.setText('Hello\n Hello\n Hello\n')
        self.main_win.tabWidget.addTab(self.main_win.editor, "test")
        self.dialog = SearchDialog(self.main_win)
    def test_perform_search(self):
        self.dialog.search_box.setText('He')
        self.dialog.perform_search()
        self.assertEqual(len(self.dialog.matches), 3)  # "is" appears twice
        self.assertEqual(self.dialog.current_match, 0)  # current match is the first one
        self.assertEqual(self.dialog.match_label.text(), '1 of 3')  # label text is correct
        self.dialog.perform_search_next()
        self.assertEqual(self.dialog.current_match, 1)

        self.dialog.perform_search_previous()
        self.assertEqual(self.dialog.current_match, 0)

        self.dialog.perform_search_previous()
        self.assertEqual(self.dialog.current_match, 2)
        
        self.dialog.perform_search_next()
        self.assertEqual(self.dialog.current_match, 0)

        self.dialog.perform_search_next()
        self.assertEqual(self.dialog.current_match, 1)

if __name__ == "__main__":
    unittest.main()
