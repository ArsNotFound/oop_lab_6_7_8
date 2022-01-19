import enum
from typing import Optional, Type, Union

from PySide6.QtCore import QPoint, QRect, QRectF, Slot
from PySide6.QtGui import QMouseEvent, Qt, QPaintEvent, QPainter, QColor
from PySide6.QtWidgets import QWidget

from model import ShapeStorage, Shape, Group

__all__ = ("PaintingArea",)

SAVE_FILE = "test.txt"


class PaintingArea(QWidget):
    class Mode(enum.Enum):
        EDIT_ITEM = enum.auto()
        INSERT_ITEM = enum.auto()

    class Direction(enum.Enum):
        UP = (0, -1, 0, 1)
        DOWN = (0, 1, 0, -1)
        LEFT = (-1, 0, -1, 0)
        RIGHT = (1, 0, 1, 0)

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._current_shape: Optional[Type[Shape]] = None
        self._mode = self.Mode.EDIT_ITEM
        self._line_color: Optional[Union[QColor, Qt.GlobalColor]] = None
        self._fill_color: Optional[Union[QColor, Qt.GlobalColor]] = None

        self._sticky_shapes: set[Shape] = set()
        self._storage: ShapeStorage = ShapeStorage(self)
        self._storage.storage_changed.connect(self.on_storage_changed)

        self._mouse_pressed = False
        self._prev_mouse_pos = QPoint()

        self.setMouseTracking(True)

    @property
    def storage(self) -> ShapeStorage:
        return self._storage

    @property
    def current_shape(self) -> Optional[Type[Shape]]:
        return self._current_shape

    @current_shape.setter
    def current_shape(self, value: Type[Shape]):
        self._current_shape = value

    @property
    def mode(self) -> Mode:
        return self._mode

    @mode.setter
    def mode(self, value: Mode):
        self._mode = value

    @property
    def line_color(self) -> Optional[Union[QColor, Qt.GlobalColor]]:
        return self._line_color

    @line_color.setter
    def line_color(self, value: Union[QColor, Qt.GlobalColor]):
        self._line_color = value

    @property
    def fill_color(self) -> Optional[Union[QColor, Qt.GlobalColor]]:
        return self._fill_color

    @fill_color.setter
    def fill_color(self, value: Union[QColor, Qt.GlobalColor]):
        self._fill_color = value

    @Slot()
    def on_storage_changed(self):
        self.update()

    def change_border_color_selected(self):
        for shape in self._storage:
            if shape.selected:
                shape.default_border_color = self._line_color

    def change_fill_color_selected(self):
        for shape in self._storage:
            if shape.selected:
                shape.default_background_color = self._fill_color

    def delete_selected(self):
        self._storage.first()
        while not self._storage.eol():
            shape = self._storage.get_current()
            if shape.selected:
                self._storage.pop_current()
            else:
                self._storage.next()

    def change_z_selected(self, z: int):
        shapes = []
        self._storage.first()
        while not self._storage.eol():
            shape = self._storage.get_current()
            if shape.selected:
                self._storage.pop_current()
                shapes.append(shape)
            else:
                self._storage.next()

        for shape in shapes:
            shape._z = z
            self._storage.push(shape, z)

    def group_selected(self):
        group = Group()
        self._storage.first()
        while not self._storage.eol():
            shape = self._storage.get_current()
            if shape.selected:
                shape.sticky = False
                self._sticky_shapes.discard(shape)
                self._storage.pop_current()
                group.add_shape(shape)
            else:
                self._storage.next()

        group.selected = True
        if len(group.shapes()) == 0:
            return
        self._storage.push(group)

    def ungroup_selected(self):
        shapes = []
        self._storage.first()
        while not self._storage.eol():
            shape = self._storage.get_current()
            if shape.selected and isinstance(shape, Group):
                self._storage.pop_current()
                shapes.extend(shape.shapes())
            else:
                self._storage.next()

        for shape in shapes:
            shape.selected = True
            self._storage.push(shape)

    def make_sticky_selected(self):
        for s in self._storage:
            if s.selected:
                s.sticky = not s.sticky
                if s.sticky:
                    self._sticky_shapes.add(s)
                else:
                    self._sticky_shapes.discard(s)

    def move_selected(self, direction: Direction, increased_step: bool = False):
        dx, dy, *_ = direction.value
        if increased_step:
            dx *= 10
            dy *= 10
        self._change_selected(dx, dy, 0, 0, 0)

    def resize_selected(self, direction: Direction, increased_step: bool = False):
        *_, dw, dh = direction.value
        if increased_step:
            dw *= 10
            dh *= 10
        self._change_selected(0, 0, dw, dh, 0)

    def rotate_selected(self, direction: Direction, increased_step: bool = False):
        if direction == self.Direction.LEFT:
            da = -5
        elif direction == self.Direction.RIGHT:
            da = 5
        else:
            return

        if increased_step:
            da *= 3

        self._change_selected(0, 0, 0, 0, da)

    def _change_selected(self, dx: int, dy: int, dw: int, dh: int, da: float):
        for shape in self._storage:
            if shape.selected:
                shape.x += dx
                shape.y += dy
                shape.w += dw
                shape.h += dh
                shape.a += da

                if not self.inside_area(shape.bounding_rect):
                    shape.x -= dx
                    shape.y -= dy
                    shape.w -= dw
                    shape.h -= dh
                    shape.a -= da

                self._check_sticky(shape)

    def _check_sticky(self, shape: Shape):
        if shape.sticky:
            for s in self._storage:
                if s == shape:
                    continue
                if shape.bounding_rect.intersects(s.bounding_rect):
                    s.sticky_shape = shape
        else:
            found = False
            for st in self._sticky_shapes:
                if shape == st:
                    continue

                if st.bounding_rect.intersects(shape.bounding_rect):
                    shape.sticky_shape = st
                    found = True

            if not found:
                shape.sticky_shape = None

    def inside_area(self, rect: QRect) -> bool:
        r = QRectF(self.rect())
        return r.contains(rect)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        x = event.x()
        y = event.y()
        ctrl = event.modifiers() & Qt.ControlModifier

        match self._mode:
            case self.Mode.EDIT_ITEM:
                self._mouse_pressed = True
                self._prev_mouse_pos = event.pos()

                flag = False
                for shape in reversed(self._storage):
                    if shape.inside(QPoint(x, y)) and not flag:
                        shape.selected = True
                        flag = True
                    elif not ctrl:
                        shape.selected = False

            case self.Mode.INSERT_ITEM:
                shape = self._current_shape(x, y, 40, 40)

                if shape.x < shape.w // 2:
                    shape.x = shape.w // 2

                if shape.x > self.width() - shape.w // 2:
                    shape.x = self.width() - shape.w // 2

                if shape.y < shape.h // 2:
                    shape.y = shape.h // 2

                if shape.y > self.height() - shape.h // 2:
                    shape.y = self.height() - shape.h // 2

                shape.default_background_color = self._fill_color
                shape.default_border_color = self._line_color
                shape.selected = True
                if not ctrl:
                    for s in self._storage:
                        s.selected = False
                self._storage.push(shape)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self._mouse_pressed = False

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if not self._mouse_pressed:
            return

        d = event.pos() - self._prev_mouse_pos
        dx = d.x()
        dy = d.y()
        self._prev_mouse_pos = event.pos()

        inside_selected = False
        for shape in self._storage:
            if shape.selected and shape.inside(self._prev_mouse_pos):
                inside_selected = True
                break

        if inside_selected:
            self._change_selected(dx, dy, 0, 0, 0)

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        painter.fillRect(0, 0, self.width(), self.height(), Qt.white)

        for shape in self._storage:
            painter.save()
            shape.paint(painter)
            painter.restore()
        painter.end()

    def save(self, filename: str):
        with open(filename, "w") as f:
            self._storage.save(f)

    def load(self, filename: str):
        try:
            with open(filename, "r") as f:
                self._storage.load(f)
            self.update()
        except FileNotFoundError:
            pass
