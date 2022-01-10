from abc import ABC, abstractmethod

from PySide6.QtGui import QPainter, QColor, Qt, QBrush, QPen, QPixmap, QPainterPath

__all__ = ("Shape",)


class Shape(ABC):
    def __init__(self, x: int, y: int, w: int, h: int):
        self._x = x
        self._y = y
        self._w = w
        self._h = h
        self._selected = False

        self._default_border_color = QColor(Qt.black)
        self._default_background_color = QColor(Qt.lightGray)

        self._selected_border_color = QColor(Qt.darkBlue)
        self._selected_background_color = QColor(Qt.transparent)

        self._default_pen = QPen(self._default_border_color)
        self._default_brush = QBrush(self._default_background_color)

        self._selected_pen = QPen(self._selected_border_color, 1.25, Qt.DotLine)
        self._selected_brush = QBrush(self._selected_background_color)

    def inside_selection(self, x: int, y: int) -> bool:
        return self.inside(x, y) or self._selected and 0 <= x - self._x <= self._w and 0 <= y - self._y <= self._h

    def paint(self, painter: QPainter):
        painter.setPen(self._default_pen)
        painter.setBrush(self._default_brush)
        painter.drawPath(self.shape())

        if self._selected:
            painter.setPen(self._selected_pen)
            painter.setBrush(self._selected_brush)
            painter.drawRect(self._x - self._w // 2, self._y - self._h // 2, self._w, self._h)

    @abstractmethod
    def inside(self, x: int, y: int) -> bool:
        pass

    @abstractmethod
    def shape(self) -> QPainterPath:
        pass

    @staticmethod
    @abstractmethod
    def name() -> str:
        pass

    @staticmethod
    @abstractmethod
    def image() -> QPixmap:
        pass

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
    def default_border_color(self) -> QColor:
        return self._default_border_color

    @default_border_color.setter
    def default_border_color(self, value: QColor):
        self._default_border_color = value
        self._default_pen.setColor(value)

    @property
    def default_background_color(self) -> QColor:
        return self._default_background_color

    @default_background_color.setter
    def default_background_color(self, value: QColor):
        self._default_background_color = value
        self._default_brush.setColor(value)

    @property
    def selected_border_color(self) -> QColor:
        return self._selected_border_color

    @selected_border_color.setter
    def selected_border_color(self, value: QColor):
        self._selected_border_color = value
        self._selected_pen.setColor(value)

    @property
    def selected_background_color(self) -> QColor:
        return self._selected_background_color

    @selected_background_color.setter
    def selected_background_color(self, value: QColor):
        self._selected_background_color = value
        self._selected_brush.setColor(value)
