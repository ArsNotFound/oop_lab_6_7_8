from PySide6.QtGui import QPainter, QPixmap, Qt, QPen, QPainterPath

from model.shape import Shape

__all__ = ("Rectangle",)


class Rectangle(Shape):
    def shape(self) -> QPainterPath:
        path = QPainterPath()
        path.addRect(-self._w // 2, -self._h // 2, self._w, self._h)

        path = self.transform.map(path)
        return path

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
