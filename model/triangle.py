from PySide6.QtCore import QPoint, Qt
from PySide6.QtGui import QPixmap, QPainterPath, QPolygon, QPainter, QPen

from model import Shape

__all__ = ("Triangle",)


class Triangle(Shape):
    def inside(self, x: int, y: int) -> bool:
        return self.polygon.containsPoint(QPoint(x, y), Qt.FillRule.OddEvenFill)

    def shape(self) -> QPainterPath:
        p0 = QPoint(-self.w // 2, self.h // 2)
        p1 = QPoint(self.w // 2, self.h // 2)
        p2 = QPoint(0, -self.h // 2)

        polygon = QPolygon()

        polygon << p0 << p1 << p2 << p0

        path = QPainterPath()
        path.addPolygon(polygon)

        return path

    @property
    def polygon(self) -> QPolygon:
        p0 = QPoint(self.x - self.w // 2, self.y + self.h // 2)
        p1 = QPoint(self.x + self.w // 2, self.y + self.h // 2)
        p2 = QPoint(self.x, self.y - self.h // 2)

        polygon = QPolygon()

        polygon << p0 << p1 << p2 << p0
        return polygon

    @staticmethod
    def name() -> str:
        return "Triangle"

    @staticmethod
    def image() -> QPixmap:
        polygon = QPolygon()
        p0 = QPoint(10, 230)
        p1 = QPoint(230, 230)
        p2 = QPoint(125, 10)

        polygon << p0 << p1 << p2 << p0

        pixmap = QPixmap(250, 250)
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)
        painter.setPen(QPen(Qt.black, 10))
        painter.drawPolygon(polygon)
        painter.end()

        return pixmap
