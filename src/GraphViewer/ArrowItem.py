import sys
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsItem, QMenu, QMessageBox, QStyle,QGraphicsLineItem
from PyQt5.QtGui import QPainter, QPen, QColor, QPolygonF
from PyQt5.QtCore import Qt, QRectF, QPointF, QLineF
class Arrow(QGraphicsLineItem):
    def __init__(self, source_node, dest_node):
        super().__init__()
        self.source_node = source_node
        self.dest_node = dest_node
        self.setPen(QPen(QColor(0, 0, 0), 3))
        self.update_positions()

    def update_positions(self):
        line = QLineF(self.source_node.pos() + self.source_node.center_bottom(), 
                      self.dest_node.pos() + self.dest_node.center_top())
        self.setLine(line)
