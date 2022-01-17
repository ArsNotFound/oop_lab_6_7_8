import typing

from PySide6.QtGui import QTransform, QColor, Qt, QPen, QBrush

__all__ = ("PosMixin", "ColorMixin")


class PosMixin:
    def __init__(self, x: int, y: int, w: int, h: int, a: float):
        self._x = x
        self._y = y
        self._w = w
        self._h = h
        self._a = a

    def save_pos(self, file: typing.IO):
        file.write(" ".join(" ".join(map(str, (self.x, self.y, self.w, self.h, self.a))) + "\n"))

    def load_pos(self, file: typing.IO):
        self.x, self.y, self.w, self.h, self.a = map(int, file.readline().strip().split(" "))

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


class ColorMixin:
    def __init__(self):
        self._selected = False

        self._default_border_color = QColor(Qt.black)
        self._default_background_color = QColor(Qt.lightGray)

        self._selected_border_color = QColor(Qt.darkBlue)
        self._selected_background_color = QColor(Qt.transparent)

        self._default_pen = QPen(self._default_border_color)
        self._default_brush = QBrush(self._default_background_color)

        self._selected_pen = QPen(self._selected_border_color, 1.25, Qt.DotLine)
        self._selected_brush = QBrush(self._selected_background_color)

    def save_color(self, file: typing.IO):
        file.write(" ".join(map(lambda x: str(x.rgba()),
                                (self.default_border_color, self.default_background_color))) + "\n")

    def load_color(self, file: typing.IO):
        border_color, background_color = map(int, file.readline().strip().split(" "))
        self.default_border_color = QColor.fromRgba(border_color)
        self.default_background_color = QColor.fromRgba(background_color)

    @property
    def selected(self) -> bool:
        return self._selected

    @selected.setter
    def selected(self, value: bool):
        self._selected = value

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
