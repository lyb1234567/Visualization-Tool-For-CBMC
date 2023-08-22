import os
import sys
root_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root_folder)
from PyQt5.QtWidgets import QApplication
from GraphViewer.NodeItem import Node
from GraphViewer.ArrowItem import Arrow
from JsonViwer.TreeViewer import Graph,MyGraphicsView
import json 
import unittest
from loguru import logger
from log_decorator import log_on_success,count_function
import log_decorator
app = QApplication([])
log_path = "/home/mirage/Visualization-Tool-For-CBMC/src/test/log_GraphViewer/log_graphviewer.log"
logger.add(log_path, rotation="500 MB")  # 每当日志大小超过500MB时，就会创建一个新的日志文件
class TestGraphViewer(unittest.TestCase):

    @log_on_success
    @count_function
    def test_node(self):
        """
        测试 Node 类的基础功能：
        - 节点能正确地初始化其文本
        - 节点的颜色状态能正确地切换
        """
        node = Node("Test Node")
        self.assertEqual(node.text, "Test Node")
        self.assertFalse(node.is_colored())
        node.colorNode()
        self.assertTrue(node.is_colored())
        node.clearNode()
        self.assertFalse(node.is_colored())

    @log_on_success
    @count_function
    def test_arrow(self):
        """
        测试 Arrow 类的基础功能：
        - 能正确地初始化其起点和终点
        - 能根据起点和终点设置其位置
        """
        source_node = Node("Source")
        dest_node = Node("Destination")
        arrow = Arrow(source_node, dest_node)
        self.assertEqual(arrow.source_node, source_node)
        self.assertEqual(arrow.dest_node, dest_node)
        self.assertEqual(arrow.line().p1(), source_node.pos() + source_node.center_bottom())
        self.assertEqual(arrow.line().p2(), dest_node.pos() + dest_node.center_top())

    @log_on_success
    @count_function
    def test_graph(self):
        """
        测试 Graph 类的基础功能：
        - 能正确地添加节点到场景
        - 能找到第一个着色的节点
        """
        scene = Graph()
        node = Node("Node in Graph")
        scene.addItem(node)
        self.assertIsNone(scene.find_first_colored())
        node.colorNode()
        self.assertEqual(scene.find_first_colored(), node)

    @log_on_success
    @count_function
    def test_graphics_view(self):
        """
        测试 MyGraphicsView 类的基础功能：
        - 能正确地将视图的中心设置在节点上
        - 能根据节点的位置滚动视图
        """
        scene = Graph()
        scene.setSceneRect(-500, -500, 1000, 1000)
        view = MyGraphicsView(scene)
        node = Node("Node in View")
        scene.addItem(node)

        # 这里是手动设置视图中心的位置
        view.centerOn(node)

        node.colorNode()
        view.scroll_to_item(node)

        # 获取视图中心的场景坐标
        view_center = view.mapToScene(view.viewport().rect().center())

        # 检查该点是否在节点的边界内
        self.assertTrue(node.boundingRect().contains(view_center - node.pos()))



if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])
        
        # 使用TextTestRunner来执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)
    current_file_path = os.path.abspath(__file__)
    with open('/home/mirage/Visualization-Tool-For-CBMC/src/test/test_graph_viewer/test_results.txt', 'a') as file:
                file.write(f'{log_decorator.module_test_count}\n')
        
            
