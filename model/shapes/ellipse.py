from PySide6.QtGui import QPainter, Qt, QPixmap, QPen, QPainterPath

from model.shape import Shape

__all__ = ("Ellipse",)


class Ellipse(Shape):
    def path(self) -> QPainterPath:
        path = QPainterPath()
        path.addEllipse(-self.w // 2, -self.h // 2, self.w, self.h)

        path = self.transform.map(path)
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
        painter.end()

        return pixmap
