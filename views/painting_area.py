from typing import Optional

from PySide6.QtGui import QMouseEvent, Qt, QPaintEvent, QPainter, QKeyEvent
from PySide6.QtWidgets import QWidget

from model import Ellipse, Storage, Shape

__all__ = ("PaintingArea",)

from model.rectangle import Rectangle


class PaintingArea(QWidget):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._storage: Storage[Shape] = Storage()
        self.setFocusPolicy(Qt.StrongFocus)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        x = event.x()
        y = event.y()
        ctrl = event.modifiers() == Qt.ControlModifier

        flag = False
        self._storage.first()
        while not self._storage.eol():
            c = self._storage.get_current()
            if c.inside(x, y) and not flag:
                c.selected = not c.selected
                flag = True
            elif not ctrl:
                c.selected = False
            self._storage.next()

        if not flag:
            if event.button() == Qt.LeftButton:
                c = Ellipse(x, y)
            else:
                c = Rectangle(x, y, 40, 40)
            c.selected = True
            self._storage.push_back(c)

        self.update()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Delete:
            self._storage.first()
            while not self._storage.eol():
                c = self._storage.get_current()
                if c.selected:
                    self._storage.pop_current()
                else:
                    self._storage.next()
            self.update()

        super().keyPressEvent(event)

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        self._storage.first()
        while not self._storage.eol():
            c = self._storage.get_current()
            painter.save()
            c.paint(painter)
            painter.restore()
            self._storage.next()