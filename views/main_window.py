from PySide6.QtWidgets import QMainWindow

from views.main_window_ui import Ui_MainWindow
from .painting_area import PaintingArea

__all__ = ("MainWindow",)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)
        self._painting_area = PaintingArea()
        self._ui.centralwidget.layout().addWidget(self._painting_area)
