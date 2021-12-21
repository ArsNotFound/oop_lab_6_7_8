from PySide6.QtGui import QPainter, QPixmap, Qt, QPen

from .shape import Shape

__all__ = ("Rectangle",)


class Rectangle(Shape):
    def __init__(self, x: int, y: int, w: int, h: int):
        super(Rectangle, self).__init__(x, y)
        self._w = w
        self._h = h

    @property
    def w(self) -> int:
        return self._w

    @w.setter
    def w(self, w: int):
        self._w = w

    @property
    def h(self) -> int:
        return self._h

    @h.setter
    def h(self, h: int):
        self._h = h

    @staticmethod
    def name() -> str:
        return "Rectangle"

    def inside(self, x: int, y: int) -> bool:
        return 0 <= x - self._x <= self._w and 0 <= y - self._y <= self._h

    def paint(self, painter: QPainter):
        painter.setPen(self._default_pen)
        painter.setBrush(self._default_brush)
        painter.drawRect(self._x, self._y, self._w, self._h)

        if self._selected:
            painter.setPen(self._selected_pen)
            painter.setBrush(self._selected_brush)
            painter.drawRect(self._x, self._y, self._w, self._h)

    @staticmethod
    def image() -> QPixmap:
        pixmap = QPixmap(250, 250)
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)
        painter.setPen(QPen(Qt.black, 2))
        painter.drawEllipse(0, 0, 250, 250)

        return pixmap
