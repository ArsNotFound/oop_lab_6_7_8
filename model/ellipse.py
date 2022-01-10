from PySide6.QtGui import QPainter, Qt, QPixmap, QPen, QPainterPath

__all__ = ("Ellipse",)

from .shape import Shape


class Ellipse(Shape):
    def inside(self, x: int, y: int) -> bool:
        return (2 * (self._x - x) / self._w) ** 2 + (2 * (self._y - y) / self._h) ** 2 <= 1

    def shape(self) -> QPainterPath:
        path = QPainterPath()
        path.addEllipse(self._x - self._w // 2, self._y - self._h // 2, self._w, self._h)
        return path

    @staticmethod
    def name() -> str:
        return "Ellipse"

    @staticmethod
    def image() -> QPixmap:
        pixmap = QPixmap(250, 250)
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)
        painter.setPen(QPen(Qt.black, 10))
        painter.drawEllipse(10, 10, 230, 230)

        return pixmap
