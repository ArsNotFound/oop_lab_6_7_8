from PySide6.QtGui import QPixmap, QPainterPath, QPainter

from model import Shape


class Group(Shape):
    def __init__(self):
        super(Group, self).__init__(0, 0, 0, 0, 0)
        self._shapes: list[Shape] = []

    def add_shape(self, shape: Shape):
        self._shapes.append(shape)

    def del_shape(self, shape: Shape):
        self._shapes.remove(shape)

    def path(self) -> QPainterPath:
        path = QPainterPath()
        for shape in self._shapes:
            path.addPath(shape.path())

        path = self.transform.map(path)
        return path

    def paint(self, painter: QPainter):
        for shape in self._shapes:
            painter.save()
            shape.paint(painter)
            painter.restore()

    @staticmethod
    def name() -> str:
        return "Group"

    @staticmethod
    def image() -> QPixmap:
        raise NotImplemented

    @property
    def x(self) -> int:
        return int(self.bounding_rect.center().x())

    @x.setter
    def x(self, value: int):
        dx = value - self.x
        for shape in self._shapes:
            shape.x += dx

    @property
    def y(self) -> int:
        return int(self.bounding_rect.center().y())

    @y.setter
    def y(self, value: int):
        dy = value - self.y
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




