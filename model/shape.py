from abc import ABC, abstractmethod

from PySide6.QtGui import QPainter, QColor, Qt, QBrush, QPen, QPixmap

__all__ = ("Shape",)


class Shape(ABC):
    _default_border_color = QColor(Qt.black)
    _default_background_color = QColor(Qt.lightGray)

    _selected_border_color = QColor(Qt.darkBlue)
    _selected_background_color = QColor(Qt.transparent)

    _default_pen = QPen(_default_border_color)
    _default_brush = QBrush(_default_background_color)

    _selected_pen = QPen(_selected_border_color, 1.25, Qt.DotLine)
    _selected_brush = QBrush(_selected_background_color)

    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y
        self._selected = False

    @abstractmethod
    def inside(self, x: int, y: int) -> bool:
        pass

    @abstractmethod
    def paint(self, painter: QPainter):
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
