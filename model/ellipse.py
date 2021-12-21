from PySide6.QtCore import QPoint
from PySide6.QtGui import QPainter, Qt, QPixmap, QPen

__all__ = ("Ellipse",)

from .shape import Shape


class Ellipse(Shape):
    def __init__(self, x: int, y: int, r: int = 20):
        super().__init__(x, y)
        self._r = r

        self._selected = False

    @property
    def r(self) -> int:
        return self._r

    @r.setter
    def r(self, r: int):
        self._r = r

    @staticmethod
    def name() -> str:
        return "Ellipse"

    def inside(self, x: int, y: int):
        return (self._x - x) ** 2 + (self._y - y) ** 2 <= self._r ** 2

    def paint(self, painter: QPainter):
        painter.setPen(self._default_pen)
        painter.setBrush(self._default_brush)
        painter.drawEllipse(QPoint(self._x, self._y), self._r, self._r)

        if self._selected:
            painter.setPen(self._selected_pen)
            painter.setBrush(self._selected_brush)
            painter.drawRect(self._x - self._r, self._y - self._r, 2 * self._r, 2 * self._r)

    @staticmethod
    def image() -> QPixmap:
        pixmap = QPixmap(250, 250)
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)
        painter.setPen(QPen(Qt.black, 2))
        painter.drawEllipse(0, 0, 250, 250)

        return pixmap
