from PySide6.QtWidgets import QTreeWidgetItem

from model import Shape, Group


def process_shape(parent: QTreeWidgetItem, shape: Shape, selected=False):
    item = ShapeTreeWidgetItem(parent, shape)
    item.setSelected(shape.selected or selected)

    if isinstance(shape, Group):
        for s in shape.shapes():
            process_shape(item, s, shape.selected or selected)


class ShapeTreeWidgetItem(QTreeWidgetItem):
    def __init__(self, parent: QTreeWidgetItem, shape: Shape):
        super(ShapeTreeWidgetItem, self).__init__(parent, [shape.name()])
        self.shape = shape
