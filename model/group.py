from PySide6.QtGui import QPixmap, QPainterPath, QPainter, QColor, QTransform

from .shape import Shape

__all__ = ("Group",)


class Group(Shape):
    def __init__(self):
        super(Group, self).__init__(0, 0, 0, 0, 0)
        self._shapes: list[Shape] = []
        self._max_x = 0
        self._max_y = 0
        self._min_x = 2**32
        self._min_y = 2**32

    def add_shape(self, shape: Shape):
        shape.selected = False
        self._max_x = max(shape.x, self._max_x)
        self._max_y = max(shape.y, self._max_y)
        self._min_x = min(shape.x, self._min_x)
        self._min_y = min(shape.y, self._min_y)

        self._shapes.append(shape)

    def shapes(self) -> list[Shape]:
        return self._shapes

    def path(self) -> QPainterPath:
        path = QPainterPath()
        for shape in self._shapes:
            p = shape.path()
            path.addPath(p)

        return path

    def paint(self, painter: QPainter):
        for shape in self._shapes:
            painter.save()
            shape.paint(painter)
            painter.restore()

        if self.selected:
            painter.setPen(self._selected_border_color)
            painter.setBrush(self._selected_background_color)
            painter.drawRect(self.bounding_rect)

    @staticmethod
    def name() -> str:
        return "Group"

    @staticmethod
    def image() -> QPixmap:
        raise NotImplemented

    @property
    def x(self) -> int:
        return (self._max_x + self._min_x) // 2

    @x.setter
    def x(self, value: int):
        dx = value - self.x
        self._max_x += dx
        self._min_x += dx
        for shape in self._shapes:
            shape.x += dx

    @property
    def y(self) -> int:
        return (self._max_y + self._min_y) // 2

    @y.setter
    def y(self, value: int):
        dy = value - self.y
        self._max_y += dy
        self._min_y += dy
        for shape in self._shapes:
            shape.y += dy

    @property
    def w(self) -> int:
        return int(self.bounding_rect.width())

    @w.setter
    def w(self, value: int):
        dw = value - self.w
        for shape in self._shapes:
            shape.w += dw

    @property
    def h(self) -> int:
        return int(self.bounding_rect.height())

    @h.setter
    def h(self, value: int):
        dh = value - self.h
        for shape in self._shapes:
            shape.h += dh

    @property
    def a(self) -> int:
        return self._a

    @a.setter
    def a(self, value: int):
        da = value - self.a
        self._a = value

        t = QTransform()
        t.translate(self.x, self.y)
        t.rotate(da)

        for shape in self._shapes:
            shape.a += da
            shape.x, shape.y = map(int, t.map(shape.x - self.x, shape.y - self.y))

    @property
    def default_border_color(self) -> QColor:
        return self._default_border_color

    @default_border_color.setter
    def default_border_color(self, value: QColor):
        self._default_border_color = value
        self._default_pen.setColor(value)
        for shape in self._shapes:
            shape.default_border_color = value

    @property
    def default_background_color(self) -> QColor:
        return self._default_background_color

    @default_background_color.setter
    def default_background_color(self, value: QColor):
        self._default_background_color = value
        self._default_brush.setColor(value)
        for shape in self._shapes:
            shape.default_background_color = value

    @property
    def selected_border_color(self) -> QColor:
        return self._selected_border_color

    @selected_border_color.setter
    def selected_border_color(self, value: QColor):
        self._selected_border_color = value
        self._selected_pen.setColor(value)
        for shape in self._shapes:
            shape.selected_border_color = value

    @property
    def selected_background_color(self) -> QColor:
        return self._selected_background_color

    @selected_background_color.setter
    def selected_background_color(self, value: QColor):
        self._selected_background_color = value
        self._selected_brush.setColor(value)
        for shape in self._shapes:
            shape.selected_background_color = value
