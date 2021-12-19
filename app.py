import sys

from PySide6.QtWidgets import QApplication

from views.main_window import MainWindow


class App(QApplication):
    def __init__(self, sys_argv: list[str]):
        super().__init__(sys_argv)
        self._main_window = MainWindow()
        self._main_window.show()


if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec())
