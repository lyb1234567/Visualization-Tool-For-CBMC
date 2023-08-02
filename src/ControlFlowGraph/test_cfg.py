from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsItem, QMenu, QAction
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtCore import QPointF,QRectF

class MyGraphicsItem(QGraphicsItem):
    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name

    # Dummy implementations of required methods
    def boundingRect(self):
        return QRectF()

    def paint(self, painter, option, widget):
        pass


class MyGraphicsView(QGraphicsView):
    def __init__(self, scene, editor_window=None):
        self.editor_window=editor_window
        super().__init__(scene)

    def contextMenuEvent(self, event):
        self.menu = QMenu(self)

        for item in self.scene().items():
            item_action = QAction(item.name, self)
            item_action.triggered.connect(lambda checked, item=item: self.scroll_to_item(item))
            self.menu.addAction(item_action)

        self.menu.popup(event.globalPos())

    def closeEvent(self, event):
        self.editor_window.terminal.clear_tracepoint()
        event.accept()

    def scroll_to_item(self, item):
        self.centerOn(item)


# Demo usage
app = QApplication([])

scene = QGraphicsScene()

# Add some named items to the scene
for i in range(10):
    item = MyGraphicsItem(f"Item {i}")
    scene.addItem(item)
    item.setPos(QPointF(i * 10, i * 10))  # Position items for visibility

editor_window = None  # Replace with your editor window
view = MyGraphicsView(scene, editor_window)
view.show()

app.exec_()
