import sys
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsItem, QMenu, QMessageBox, QStyle,QGraphicsLineItem
from PyQt5.QtGui import QPainter, QPen, QColor, QPolygonF
from PyQt5.QtCore import Qt, QRectF, QPointF, QLineF
from math import sin, cos, pi,acos

class Arrow(QGraphicsLineItem):
    def __init__(self, source_node, dest_node):
        super().__init__()
        self.source_node = source_node
        self.dest_node = dest_node
        self.setPen(QPen(QColor(0, 0, 0), 3, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        self.arrowHead = QPolygonF()
        self.update_positions()

    def update_positions(self):
        line = QLineF(self.source_node.pos() + self.source_node.center_bottom(), 
                      self.dest_node.pos() + self.dest_node.center_top())
        self.setLine(line)

    def paint(self, painter, option, widget=None):
        if self.source_node.collidesWithItem(self.dest_node):
            return

        myPen = self.pen()
        myPen.setColor(QColor(0, 0, 0))
        arrowSize = 20.0
        painter.setPen(myPen)
        painter.setBrush(QColor(0, 0, 0))

        centerLine = QLineF(self.source_node.pos(), self.dest_node.pos())
        endPolygon = self.dest_node.polygon()
        p1 = endPolygon.first() + self.dest_node.pos()

        intersectPoint = QPointF()
        for i in endPolygon:
            p2 = i + self.dest_node.pos()
            polyLine = QLineF(p1, p2)
            intersectType = polyLine.intersect(centerLine, intersectPoint)
            if intersectType == QLineF.BoundedIntersection:
                break
            p1 = p2

        self.setLine(QLineF(intersectPoint, self.source_node.pos()))

        line = self.line()
        angle = acos(line.dx() / line.length())
        if line.dy() >= 0:
            angle = (pi * 2) - angle

        arrowP1 = line.p1() + QPointF(sin(angle + pi / 3) * arrowSize,
                                      cos(angle + pi / 3) * arrowSize)
        arrowP2 = line.p1() + QPointF(sin(angle + pi - pi / 3) * arrowSize,
                                      cos(angle + pi - pi / 3) * arrowSize)

        self.arrowHead.clear()
        for point in [line.p1(), arrowP1, arrowP2]:
            self.arrowHead.append(point)

        painter.drawLine(line)
        painter.drawPolygon(self.arrowHead)

class Node(QGraphicsItem):
    def __init__(self, text):
        super().__init__()
        self.text = text
        self.arrows = []
        self.node_info={}
        self.setAcceptHoverEvents(True)
    def contextMenuEvent(self, event):
        menu = QMenu()
        action = menu.addAction("Show Info")
        action.triggered.connect(self.show_info)
        menu.exec_(event.screenPos())

    def hoverEnterEvent(self, event):
        print(f"Mouse entered {self.text}")

    def hoverLeaveEvent(self, event):
        print(f"Mouse left {self.text}")
    def show_info(self):
        print(self.info)
    def add_child(self, child):
        arrow = Arrow(self, child)
        self.arrows.append(arrow)
        return arrow

    def boundingRect(self):
        return QRectF(0, 0, 200, 50)

    def paint(self, painter, option, widget):
        painter.drawRect(0, 0, 300, 50)
        painter.drawText(0, 0, 300, 50, Qt.AlignCenter, self.text)

    def center_bottom(self):
        return QPointF(150, 50)

    def center_top(self):
        return QPointF(150, 0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    scene = QGraphicsScene()

    data = {'assertion *value > 0': ['  value=1 \n', '  value=&value!0@1 \n', '  value=0 \n', 'value=0 \n','value=0 \n','assertion *value > 0']}

    y = 0
    prev_node = None
    for statement in data['assertion *value > 0']:
        node = Node(statement)
        node.setPos(0, y)
        y += 100  # Adjust this value to change the vertical spacing between nodes
        scene.addItem(node)
        if prev_node is not None:
            arrow = Arrow(prev_node, node)
            scene.addItem(arrow)
        prev_node = node
 
    view = QGraphicsView(scene)
    view.resize(800, 600)
    view.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
    view.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
    view.show()

    sys.exit(app.exec_())
