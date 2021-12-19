from PySide6.QtCore import QPoint
from PySide6.QtGui import QPainter, Qt, QColor, QBrush, QPen

__all__ = ("Circle",)


class Circle:
    __default_border_color = QColor(Qt.black)
    __default_background_color = QColor(Qt.lightGray)

    __selected_border_color = QColor(Qt.black)
    __selected_background_color = QColor(Qt.blue)

    __default_pen = QPen(__default_border_color)
    __default_brush = QBrush(__default_background_color)

    __selected_pen = QPen(__selected_border_color)
    __selected_brush = QBrush(__selected_background_color)

    def __init__(self, x: int, y: int, r: int = 20):
        self._x = x
        self._y = y
        self._r = r

        self._selected = False

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def r(self):
        return self._r

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, value):
        self._selected = value

    @property
    def default_border_color(self) -> QColor:
        return self.__default_border_color

    @default_border_color.setter
    def default_border_color(self, value: QColor):
        self.__default_border_color = value
        self.__default_pen.setColor(value)

    @property
    def default_background_color(self) -> QColor:
        return self.__default_background_color

    @default_background_color.setter
    def default_background_color(self, value: QColor):
        self.__default_background_color = value
        self.__default_brush.setColor(value)

    @property
    def selected_border_color(self) -> QColor:
        return self.__selected_border_color

    @selected_border_color.setter
    def selected_border_color(self, value: QColor):
        self.__selected_border_color = value
        self.__selected_pen.setColor(value)

    @property
    def selected_background_color(self) -> QColor:
        return self.__selected_background_color

    @selected_background_color.setter
    def selected_background_color(self, value: QColor):
        self.__selected_background_color = value
        self.__selected_brush.setColor(value)

    def inside(self, x: int, y: int):
        return (self._x - x) ** 2 + (self._y - y) ** 2 <= self._r ** 2

    def paint(self, painter: QPainter):
        if self._selected:
            painter.setPen(self.__selected_pen)
            painter.setBrush(self.__selected_brush)
        else:
            painter.setPen(self.__default_pen)
            painter.setBrush(self.__default_brush)
        painter.drawEllipse(QPoint(self._x, self._y), self._r, self._r)
