import typing
from abc import ABC, abstractmethod

from PySide6.QtCore import QPoint
from PySide6.QtGui import QTransform, QColor, Qt, QPen, QBrush

__all__ = ("PosMixin", "ColorMixin")


class PosMixin:
    def __init__(self, x: int, y: int, w: int, h: int, a: float):
        self._x = x
        self._y = y
        self._w = w
        self._h = h
        self._a = a

    def save_pos(self, file: typing.IO) -> None:
        file.write(" ".join(map(str, (self.x, self.y, self.w, self.h, self.a))) + "\n")

    def load_pos(self, file: typing.IO) -> None:
        self.x, self.y, self.w, self.h, self.a = map(int, file.readline().strip().split(" "))

    @abstractmethod
    def _notify_pos_changed(self):
        pass

    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, value: int) -> None:
        if self._x == value:
            return
        self._x = value
        self._notify_pos_changed()

    @property
    def y(self) -> int:
        return self._y

    @property
    def pos(self) -> QPoint:
        return QPoint(self.x, self.y)

    @pos.setter
    def pos(self, value: QPoint) -> None:
        self.x = value.x()
        self.y = value.y()

    @y.setter
    def y(self, value: int) -> None:
        if self._y == value:
            return
        self._y = value
        self._notify_pos_changed()

    @property
    def w(self) -> int:
        return self._w

    @w.setter
    def w(self, value: int) -> None:
        if self._w == value:
            return
        self._w = value
        self._notify_pos_changed()

    @property
    def h(self) -> int:
        return self._h

    @h.setter
    def h(self, value: int) -> None:
        if self._h == value:
            return
        self._h = value
        self._notify_pos_changed()

    @property
    def a(self) -> float:
        return self._a

    @a.setter
    def a(self, value: float):
        if self._a == value:
            return
        self._a = value
        self._notify_pos_changed()

    @property
    def transform(self) -> QTransform:
        t = QTransform()
        t.translate(self.x, self.y)
        t.rotate(self.a)

        return t


Color: typing.TypeAlias = QColor | Qt.GlobalColor


class ColorMixin(ABC):
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

    @abstractmethod
    def _notify_default_color_changed(self):
        pass

    @abstractmethod
    def _notify_selected_color_changed(self):
        pass

    @abstractmethod
    def _notify_selected_changed(self):
        pass

    @property
    def selected(self) -> bool:
        return self._selected

    @selected.setter
    def selected(self, value: bool) -> None:
        if self._selected == value:
            return
        self._selected = value
        self._notify_selected_changed()

    @property
    def default_border_color(self) -> QColor:
        return self._default_border_color

    @default_border_color.setter
    def default_border_color(self, value: Color) -> None:
        c = QColor(value)
        if self._default_border_color == c:
            return
        self._default_border_color = c
        self._default_pen.setColor(c)
        self._notify_default_color_changed()

    @property
    def default_background_color(self) -> QColor:
        return self._default_background_color

    @default_background_color.setter
    def default_background_color(self, value: Color) -> None:
        c = QColor(value)
        if self._default_background_color == c:
            return
        self._default_background_color = c
        self._default_brush.setColor(c)
        self._notify_default_color_changed()

    @property
    def selected_border_color(self) -> QColor:
        return self._selected_border_color

    @selected_border_color.setter
    def selected_border_color(self, value: Color) -> None:
        c = QColor(value)
        if self._selected_border_color == c:
            return
        self._selected_border_color = c
        self._selected_pen.setColor(c)
        self._notify_selected_color_changed()

    @property
    def selected_background_color(self) -> QColor:
        return self._selected_background_color

    @selected_background_color.setter
    def selected_background_color(self, value: Color) -> None:
        c = QColor(value)
        if self._selected_background_color == c:
            return
        self._selected_background_color = c
        self._selected_brush.setColor(c)
        self._notify_selected_color_changed()
