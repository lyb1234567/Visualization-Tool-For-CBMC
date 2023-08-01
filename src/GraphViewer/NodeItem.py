import sys
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsItem, QMenu, QMessageBox, QStyle,QGraphicsLineItem,QToolTip
from PyQt5.QtGui import QPainter, QPen, QColor, QPolygonF
from PyQt5.QtCore import Qt, QRectF, QPointF, QLineF
import os 
root_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_folder)
from GraphViewer.ArrowItem import Arrow
from ControlFlowGraph.ControlFlowGraphGenerator import Source_Type
class Node(QGraphicsItem):
    def __init__(self, text,tree_viewer=None,cfg=None,trace_num=None,set_back_ground_flag=None):
        super().__init__()
        self.text = text
        self.arrows = []
        self.node_info={}
        self.tree_viewer=tree_viewer
        self.cfg=cfg
        self.trace_num=trace_num
        self.set_back_ground_flag=set_back_ground_flag
        self.setAcceptHoverEvents(True)
    def contextMenuEvent(self, event):
        menu = QMenu()
        action = menu.addAction("View Source File")
        action.triggered.connect(self.viewSourceFile)
        menu.exec_(event.screenPos())

    def info(self):
        result=""
        if self.node_info:
            for key in self.node_info.keys():
                if key!='assertion_statement':
                    temp="{0}:{1}".format(key,self.node_info[key])+'\n'
                    result=result+temp 
        return result 
    def hoverEnterEvent(self, event):
        info=self.info()
        QToolTip.showText(event.screenPos(),info)
    def hoverLeaveEvent(self, event):
        pass
    def viewSourceFile(self):
        filename=self.node_info['file']
        line_number=self.node_info['line']
        assertion_statement=self.node_info['assertion_statement']
        self.tree_viewer.viewSourceFile(filename,line_number,SOURCE_TYPE=Source_Type.TRACE_SOURCE,cfg=self.cfg,trace_num=self.trace_num,assertion_statement=assertion_statement)
    def add_child(self, child):
        arrow = Arrow(self, child)
        self.arrows.append(arrow)
        return arrow
    def is_colored(self):
        return self.set_back_ground_flag
    def boundingRect(self):
        return QRectF(0, 0, 200, 50)

    def paint(self, painter, option, widget):
        if not self.set_back_ground_flag:
            painter.drawRect(0, 0, 300, 50)
            painter.drawText(0, 0, 300, 50, Qt.AlignCenter, self.text)
        else:
            color = QColor(255, 0, 0)  # 创建红色
            painter.setBrush(color)
            painter.drawRect(0, 0, 300, 50)
            painter.setBrush(QColor(0, 0, 0))  # 设置文字颜色为黑色
            painter.drawText(0, 0, 300, 50, Qt.AlignCenter, self.text)


    def center_bottom(self):
        return QPointF(150, 50)

    def center_top(self):
        return QPointF(150, 0)