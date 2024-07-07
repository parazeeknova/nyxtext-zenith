from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow

from .framework.titleBar import CustomTitleBar
from .scripts.def_path import resource


class Zenith(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowTitle("Zenith")
        self.setGeometry(100, 100, 800, 600)

        self.setWindowIcon(QIcon(resource("..\\media\\icon.ico")))

        self.titleBar = CustomTitleBar(self)
        self.setMenuWidget(self.titleBar)
