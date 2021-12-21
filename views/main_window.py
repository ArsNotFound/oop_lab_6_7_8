from PySide6.QtCore import Slot
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QToolBox, QToolBar

__all__ = ("MainWindow",)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._create_actions()
        self._create_toolbars()

        self.setWindowTitle("OOP LAB 6")
        self.addToolBar(self._edit_toolbar)

        self._central_widget = QWidget()
        self._central_widget.setMinimumSize(800, 600)

        self._layout = QHBoxLayout()
        self._central_widget.setLayout(self._layout)

        self.setCentralWidget(self._central_widget)

    def _create_actions(self):
        self._delete_action = QAction(QIcon("resources/images/delete.png"), "Delete")
        self._delete_action.setShortcut("Delete")
        self._delete_action.triggered.connect(self._delete_item)

    def _create_toolbars(self):
        self._edit_toolbar = QToolBar()

        self._edit_toolbar.addAction(self._delete_action)

    @Slot()
    def _delete_item(self):
        pass
