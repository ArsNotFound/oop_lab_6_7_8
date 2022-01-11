from PySide6.QtCore import QRect
from PySide6.QtGui import QPainter, QPixmap, Qt, QPen, QPainterPath

from .shape import Shape

__all__ = ("Rectangle",)


class Rectangle(Shape):
    def inside(self, x: int, y: int) -> bool:
        return self.rect.contains(x, y)

    def shape(self) -> QPainterPath:
        path = QPainterPath()
        path.addRect(QRect(-self._w // 2,  -self._h // 2, self._w, self._h))
        return path

    @property
    def rect(self) -> QRect:
        return QRect(self._x - self._w // 2, self._y - self._h // 2, self._w, self._h)

    @staticmethod
    def name() -> str:
        return "Rectangle"

    @staticmethod
    def image() -> QPixmap:
        pixmap = QPixmap(250, 250)
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)
        painter.setPen(QPen(Qt.black, 10))
        painter.drawRect(10, 10, 230, 230)
        painter.end()

        return pixmap
