import functools
from typing import Type, Callable, Union

from PySide6.QtCore import Slot, QSize, QRect
from PySide6.QtGui import QIcon, Qt, QAction, QKeySequence, QColor, QPixmap, QPainter, QKeyEvent
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QButtonGroup, QAbstractButton, QToolButton, \
    QGridLayout, QLabel, QToolBox, QSizePolicy, QMenu

__all__ = ("MainWindow",)

import model
from views import PaintingArea

COLORS = {
    "Black": Qt.black,
    "White": Qt.white,
    "Red": Qt.red,
    "Blue": Qt.blue,
    "Yellow": Qt.yellow,
    "Green": Qt.green,
}

Color = Union[QColor, Qt.GlobalColor]

DELETE_PATH = "resources/images/delete.png"
EDIT_PATH = "resources/images/pointer.png"
FLOODFILL_PATH = "resources/images/floodfill.png"
LINECOLOR_PATH = "resources/images/linecolor.png"
BRING_TO_FRONT_PATH = "resources/images/bringtofront.png"
SEND_TO_BACK_PATH = "resources/images/sendtoback.png"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self._create_tool_box()
        self._create_actions()
        self._create_toolbars()

        self._area = PaintingArea()
        self._area.line_color = self._line_color
        self._area.fill_color = self._fill_color

        layout = QHBoxLayout()
        layout.addWidget(self._toolbox)
        layout.addWidget(self._area)

        widget = QWidget()
        widget.setLayout(layout)
        widget.setMinimumSize(800, 600)
        self.setFocusPolicy(Qt.StrongFocus)

        self.setCentralWidget(widget)
        self.setWindowTitle("OOP LAB 6")

    def _delete_item(self):
        self._area.delete_selected()

    def _bring_to_front(self):
        self._area.change_z_selected(100)

    def _send_to_back(self):
        self._area.change_z_selected(-100)

    def _set_edit_mode(self):
        self._area.mode = PaintingArea.Mode.EDIT_ITEM
        self._edit_action.setChecked(True)
        for btn in self._button_group.buttons():
            btn.setChecked(False)

    def _set_insert_mode(self, shape: Type[model.Shape]):
        self._area.current_shape = shape
        self._area.mode = PaintingArea.Mode.INSERT_ITEM
        self._edit_action.setChecked(False)

    def _fill_button_clicked(self):
        self._area.change_color_selected()

    def _line_button_clicked(self):
        self._area.change_color_selected()

    def _item_color_changed(self, color: Color):
        self._fill_color = color
        self._fill_color_tool_button.setIcon(
            self._create_color_tool_button_icon(FLOODFILL_PATH, self._fill_color)
        )
        self._area.fill_color = color

    def _line_color_changed(self, color: Color):
        self._line_color = color
        self._line_color_tool_button.setIcon(
            self._create_color_tool_button_icon(LINECOLOR_PATH, self._line_color)
        )
        self._area.line_color = color

    @Slot(QAbstractButton)
    def _button_group_clicked(self, button: QAbstractButton):
        buttons = self._button_group.buttons()
        button.setChecked(True)
        for b in buttons:
            if b != button:
                b.setChecked(False)

        ids = self._button_group.id(button)
        self._set_insert_mode(self._shapes_id[ids])

    def keyPressEvent(self, event: QKeyEvent) -> None:
        ctrl = bool(event.modifiers() & Qt.ControlModifier)
        if event.modifiers() & Qt.ShiftModifier:
            match event.key():
                case Qt.Key_Up:
                    self._area.resize_selected(PaintingArea.Direction.UP, ctrl)
                case Qt.Key_Down:
                    self._area.resize_selected(PaintingArea.Direction.DOWN, ctrl)
                case Qt.Key_Left:
                    self._area.resize_selected(PaintingArea.Direction.LEFT, ctrl)
                case Qt.Key_Right:
                    self._area.resize_selected(PaintingArea.Direction.RIGHT, ctrl)

        else:
            match event.key():
                case Qt.Key_Up:
                    self._area.move_selected(PaintingArea.Direction.UP, ctrl)
                case Qt.Key_Down:
                    self._area.move_selected(PaintingArea.Direction.DOWN, ctrl)
                case Qt.Key_Left:
                    self._area.move_selected(PaintingArea.Direction.LEFT, ctrl)
                case Qt.Key_Right:
                    self._area.move_selected(PaintingArea.Direction.RIGHT, ctrl)

        super().keyPressEvent(event)

    def _create_tool_box(self):
        self._button_group = QButtonGroup(self)
        self._button_group.setExclusive(False)
        self._button_group.buttonClicked.connect(self._button_group_clicked)
        self._shapes_id: dict[int, Type[model.Shape]] = {}
        self._last_btn_id = -1

        layout = QGridLayout()
        i = 0
        for s in model.available_shapes:
            layout.addWidget(self._create_cell_widget(s), i // 2, i % 2)
            i += 1

        widget = QWidget()
        widget.setLayout(layout)

        self._toolbox = QToolBox()
        self._toolbox.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Ignored))
        self._toolbox.addItem(widget, "Shapes")

    def _create_actions(self):
        self._delete_action = QAction(QIcon(DELETE_PATH), "Delete", self)
        self._delete_action.setShortcut("Delete")
        self._delete_action.triggered.connect(self._delete_item)

        self._edit_action = QAction(QIcon(EDIT_PATH), "Edit", self)
        self._edit_action.triggered.connect(self._set_edit_mode)
        self._edit_action.setCheckable(True)

        self._bring_to_front_action = QAction(QIcon(BRING_TO_FRONT_PATH), "Bring to front", self)
        self._bring_to_front_action.setShortcut("F")
        self._bring_to_front_action.triggered.connect(self._bring_to_front)

        self._send_to_back_action = QAction(QIcon(SEND_TO_BACK_PATH), "Send to back", self)
        self._send_to_back_action.setShortcut("B")
        self._send_to_back_action.triggered.connect(self._send_to_back)

        self._exit_action = QAction("Exit", self)
        self._exit_action.setShortcut(QKeySequence.Quit)
        self._exit_action.triggered.connect(QWidget.close)

    def _create_toolbars(self):
        self._edit_toolbar = self.addToolBar("Edit")
        self._edit_toolbar.addAction(self._delete_action)
        self._edit_toolbar.addAction(self._bring_to_front_action)
        self._edit_toolbar.addAction(self._send_to_back_action)
        self._edit_toolbar.addAction(self._edit_action)

        self._fill_color = Qt.white
        self._fill_color_tool_button = QToolButton()
        self._fill_color_tool_button.setPopupMode(QToolButton.MenuButtonPopup)
        self._fill_color_tool_button.setMenu(self._create_color_menu(self._item_color_changed, self._fill_color))
        self._fill_color_tool_button.setIcon(
            self._create_color_tool_button_icon(FLOODFILL_PATH, self._fill_color)
        )

        self._fill_color_tool_button.clicked.connect(self._fill_button_clicked)

        self._line_color = Qt.black
        self._line_color_tool_button = QToolButton()
        self._line_color_tool_button.setPopupMode(QToolButton.MenuButtonPopup)
        self._line_color_tool_button.setMenu(self._create_color_menu(self._line_color_changed, self._line_color))
        self._line_color_tool_button.setIcon(
            self._create_color_tool_button_icon(LINECOLOR_PATH, self._line_color)
        )

        self._line_color_tool_button.clicked.connect(self._line_button_clicked)

        self._color_toolbar = self.addToolBar("Color")
        self._color_toolbar.addWidget(self._fill_color_tool_button)
        self._color_toolbar.addWidget(self._line_color_tool_button)

    def _create_cell_widget(self, shape: Type[model.Shape]) -> QWidget:
        icon = QIcon(shape.image())

        button = QToolButton()
        button.setIcon(icon)
        button.setIconSize(QSize(50, 50))
        button.setCheckable(True)
        self._last_btn_id += 1
        self._button_group.addButton(button, self._last_btn_id)
        self._shapes_id[self._last_btn_id] = shape

        layout = QGridLayout()
        layout.addWidget(button, 0, 0, Qt.AlignHCenter)
        layout.addWidget(QLabel(shape.name()), 1, 0, Qt.AlignCenter)

        widget = QWidget()
        widget.setLayout(layout)

        return widget

    def _create_color_menu(self, func: Callable[[Color], None], default_color: Color) -> QMenu:
        color_menu = QMenu(self)

        for name, color in COLORS.items():
            action = QAction(name, color_menu)
            action.setIcon(self._create_color_icon(color))
            action.triggered.connect(functools.partial(func, color))

            color_menu.addAction(action)
            if color == default_color:
                color_menu.setDefaultAction(action)

        return color_menu

    @staticmethod
    def _create_color_tool_button_icon(image_file: str, color: Color) -> QIcon:
        pixmap = QPixmap(50, 80)
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)
        image = QPixmap(image_file)

        source = QRect(0, 0, 42, 43)
        target = QRect(0, 4, 42, 43)

        painter.fillRect(QRect(0, 60, 50, 80), color)
        painter.drawPixmap(target, image, source)
        painter.end()

        return QIcon(pixmap)

    @staticmethod
    def _create_color_icon(color: Color) -> QIcon:
        pixmap = QPixmap(20, 20)
        pixmap.fill(color)

        return QIcon(pixmap)
