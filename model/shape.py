import typing
from abc import ABC, abstractmethod

from PySide6.QtCore import QRectF, QPoint
from PySide6.QtGui import QPainter, QColor, Qt, QBrush, QPen, QPixmap, QPainterPath, QTransform

__all__ = ("Shape",)


class Shape(ABC):
    def __init__(self, x: int, y: int, w: int, h: int, a: float):
        self._x = x
        self._y = y
        self._w = w
        self._h = h
        self._a = a
        self._selected = False

        self._default_border_color = QColor(Qt.black)
        self._default_background_color = QColor(Qt.lightGray)

        self._selected_border_color = QColor(Qt.darkBlue)
        self._selected_background_color = QColor(Qt.transparent)

        self._default_pen = QPen(self._default_border_color)
        self._default_brush = QBrush(self._default_background_color)

        self._selected_pen = QPen(self._selected_border_color, 1.25, Qt.DotLine)
        self._selected_brush = QBrush(self._selected_background_color)

    def inside(self, p: QPoint) -> bool:
        return self.path().contains(p) or self._selected and self.bounding_rect.contains(p)

    def paint(self, painter: QPainter):
        painter.setPen(self._default_pen)
        painter.setBrush(self._default_brush)
        painter.drawPath(self.path())

        if self._selected:
            painter.setPen(self._selected_pen)
            painter.setBrush(self._selected_brush)
            painter.drawRect(self.path().boundingRect())

    @abstractmethod
    def path(self) -> QPainterPath:
        pass

    @staticmethod
    @abstractmethod
    def name() -> str:
        pass

    @staticmethod
    @abstractmethod
    def image() -> QPixmap:
        pass

    @classmethod
    def load(cls, file: typing.IO) -> "Shape":
        line = file.readline()
        x, y, w, h, a, *_ = map(int, line.strip().split(" "))
        s = cls(x, y, w, h, a)

        border_color, background_color = map(int, line.strip().split(" "))
        s.default_border_color = QColor.fromRgba(border_color)
        s.default_background_color = QColor.fromRgba(background_color)

        return s

    def save(self, file: typing.IO):
        file.write(self.name() + "\n")
        file.write(" ".join(map(str, (self.x, self.y, self.w, self.h, self.a))) + "\n")
        file.write(" ".join(map(lambda x: str(x.rgba()),
                                (self.default_border_color, self.default_background_color))) + "\n")

    @property
    def selected(self) -> bool:
        return self._selected

    @selected.setter
    def selected(self, selected: bool):
        self._selected = selected

    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, x: int):
        self._x = x

    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, y: int):
        self._y = y

    @property
    def w(self) -> int:
        return self._w

    @w.setter
    def w(self, value: int):
        self._w = value

    @property
    def h(self) -> int:
        return self._h

    @h.setter
    def h(self, value: int):
        self._h = value

    @property
    def a(self) -> float:
        return self._a

    @a.setter
    def a(self, value: float):
        self._a = value

    @property
    def transform(self) -> QTransform:
        t = QTransform()
        t.translate(self.x, self.y)
        t.rotate(self.a)

        return t

    @property
    def bounding_rect(self) -> QRectF:
        return self.path().boundingRect()

    @property
    def default_border_color(self) -> QColor:
        return self._default_border_color

    @default_border_color.setter
    def default_border_color(self, value: QColor):
        self._default_border_color = QColor(value)
        self._default_pen.setColor(value)

    @property
    def default_background_color(self) -> QColor:
        return self._default_background_color

    @default_background_color.setter
    def default_background_color(self, value: QColor):
        self._default_background_color = QColor(value)
        self._default_brush.setColor(value)

    @property
    def selected_border_color(self) -> QColor:
        return self._selected_border_color

    @selected_border_color.setter
    def selected_border_color(self, value: QColor):
        self._selected_border_color = QColor(value)
        self._selected_pen.setColor(value)

    @property
    def selected_background_color(self) -> QColor:
        return self._selected_background_color

    @selected_background_color.setter
    def selected_background_color(self, value: QColor):
        self._selected_background_color = QColor(value)
        self._selected_brush.setColor(value)
