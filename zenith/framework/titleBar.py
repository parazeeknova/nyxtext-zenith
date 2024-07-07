from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget

from ..scripts.def_path import resource
from .intMenuBar import menu_bar

titleIcon = resource("..\\media\\icon.ico")
minimiseIcon = resource("..\\media\\titlebar\\minimise.svg")
maximiseIcon = resource("..\\media\\titlebar\\maximise.svg")
closeIcon = resource("..\\media\\titlebar\\close.svg")


class CustomTitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.iconLabel = QLabel(self)
        self.iconLabel.setPixmap(QIcon(titleIcon).pixmap(15, 15))
        self.iconLabel.setStyleSheet("padding-left: 5px;")
        self.layout.addWidget(self.iconLabel, 0, Qt.AlignLeft)

        self.menuBar = menu_bar(self)
        self.layout.addWidget(self.menuBar, 0)

        self.titleLabel = QLabel("Nyxtext Zenith", self)
        self.layout.addWidget(self.titleLabel, 1, Qt.AlignCenter)
        self.titleLabel.setStyleSheet(
            "color: #cad3f5; font-style: italic; font-size: 12px;"
        )

        self.minimizeButton = QPushButton(self)
        self.minimizeButton.setIcon(QIcon(minimiseIcon))
        self.minimizeButton.setIconSize(QSize(12, 12))
        self.minimizeButton.clicked.connect(parent.showMinimized)
        self.layout.addWidget(self.minimizeButton)
        self.minimizeButton.setStyleSheet(
            "QPushButton {background-color: transparent; border: none;padding: 5px;}"
        )

        self.maximizeButton = QPushButton(self)
        self.maximizeButton.setIcon(QIcon(maximiseIcon))
        self.maximizeButton.setIconSize(QSize(12, 12))
        self.maximizeButton.clicked.connect(self.toggleMaximize)
        self.layout.addWidget(self.maximizeButton)
        self.maximizeButton.setStyleSheet(
            "QPushButton {background-color: transparent; border: none;padding: 5px;}"
        )

        self.closeButton = QPushButton(self)
        self.closeButton.setIcon(QIcon(closeIcon))
        self.closeButton.setIconSize(QSize(12, 12))
        self.closeButton.clicked.connect(parent.close)
        self.layout.addWidget(self.closeButton)
        self.closeButton.setStyleSheet(
            "QPushButton {background-color: transparent; border: none;padding: 5px;}"
        )

        self.setLayout(self.layout)

    def toggleMaximize(self):
        if self.parent().isMaximized():
            self.parent().showNormal()
        else:
            self.parent().showMaximized()

    def mouseDoubleClickEvent(self, event):
        self.toggleMaximize()
