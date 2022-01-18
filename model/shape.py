import typing
from abc import abstractmethod, ABCMeta

from PySide6.QtCore import QRectF, QPoint, QObject, Signal, Slot
from PySide6.QtGui import QPainter, QPixmap, QPainterPath, QPen, Qt

from .mixins import PosMixin, ColorMixin

__all__ = ("Shape",)


class MyMeta(type(QObject), ABCMeta):
    pass


class Shape(QObject, PosMixin, ColorMixin, metaclass=MyMeta):
    changed = Signal(object)

    def __init__(self, x: int = 0, y: int = 0, w: int = 0, h: int = 0, a: float = 0,
                 parent: typing.Optional[QObject] = None):
        QObject.__init__(self, parent)
        PosMixin.__init__(self, x, y, w, h, a)
        ColorMixin.__init__(self)

        self._sticky = False
        self._sticky_prev_pos: QPoint = QPoint()
        self._sticky_shape: typing.Optional[Shape] = None

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

    @property
    def bounding_rect(self) -> QRectF:
        return self.path().boundingRect()

    def inside(self, p: QPoint) -> bool:
        return self.path().contains(p) or self._selected and self.bounding_rect.contains(p)

    def paint(self, painter: QPainter) -> None:
        painter.setPen(self._default_pen)
        painter.setBrush(self._default_brush)
        painter.drawPath(self.path())

        if self._selected:
            painter.setPen(self._selected_pen)
            painter.setBrush(self._selected_brush)
            painter.drawRect(self.bounding_rect)

        if self._sticky:
            painter.setPen(QPen(Qt.black, 4))
            painter.drawRect(self.bounding_rect)

    @property
    def sticky(self) -> bool:
        return self._sticky

    @sticky.setter
    def sticky(self, value: bool) -> None:
        if self._sticky == value:
            return
        self._sticky = value
        self.changed.emit(self)

    @property
    def sticky_shape(self) -> typing.Optional["Shape"]:
        return self._sticky_shape

    @sticky_shape.setter
    def sticky_shape(self, value: typing.Optional["Shape"]) -> None:
        if self._sticky_shape:
            self._sticky_shape.changed.disconnect(self.sticky_changed)

        self._sticky_shape = value

        if self._sticky_shape:
            self._sticky_shape.changed.connect(self.sticky_changed)
            self._sticky_prev_pos = self._sticky_shape.pos

    @Slot(object)
    def sticky_changed(self, sticky: "Shape"):
        if not sticky._sticky:
            sticky.changed.disconnect(self.sticky_changed)
            self._sticky_shape = None

        d = self.pos - self._sticky_prev_pos
        self.pos = sticky.pos + d
        self._sticky_prev_pos = sticky.pos

    @classmethod
    def load(cls, file: typing.IO) -> "Shape":
        s = cls()
        s.selected, s.sticky = map(bool, map(int, file.readline().strip().split(" ")))
        s.load_pos(file)
        s.load_color(file)

        return s

    def save(self, file: typing.IO) -> None:
        file.write(self.name() + "\n")
        file.write("1" if self.selected else "0")
        file.write(" ")
        file.write("1" if self.sticky else "0")
        file.write("\n")
        self.save_pos(file)
        self.save_color(file)

    def _notify_pos_changed(self):
        self.changed.emit(self)

    def _notify_selected_changed(self):
        self.changed.emit(self)

    def _notify_default_color_changed(self):
        self.changed.emit(self)

    def _notify_selected_color_changed(self):
        self.changed.emit(self)
