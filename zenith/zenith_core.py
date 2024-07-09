from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow, QSplitter, QTextEdit, QVBoxLayout, QWidget

from .components.rightSideBar import FileTreeWidget
from .components.tabTopbar import tabRow
from .framework.statusBar import ZenithStatusBar
from .framework.titleBar import CustomTitleBar
from .scripts.def_path import resource
from .scripts.shortcuts import key_shortcuts


class Zenith(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowTitle("Zenith")
        self.setGeometry(100, 100, 800, 600)

        self.setWindowIcon(QIcon(resource(r"../media/icon.ico")))

        self.titleBar = CustomTitleBar(self)  # Title bar or the top bar
        self.setMenuWidget(self.titleBar)

        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        layout = QVBoxLayout(centralWidget)

        splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(splitter)

        tabRow(self, splitter)  # Tab row or the top bar

        fileTree = FileTreeWidget()
        splitter.addWidget(fileTree)

        self.statusBar = ZenithStatusBar(self, self)  # Status bar or the bottom bar
        self.setStatusBar(self.statusBar)

        key_shortcuts(self)  # Keyboard shortcuts defined in shortcuts.json
        splitter.setSizes([600, 150])  # Set the initial size of the splitter panes

    def addNewTab(self, content=""):
        newTab = QTextEdit()
        newTab.setStyleSheet("QTextEdit {border: none;}")
        if isinstance(content, str):
            newTab.setText(content)
        else:
            newTab.setText("")
        tabIndex = self.tabWidget.addTab(newTab, "Document")
        self.tabWidget.setCurrentIndex(tabIndex)

    def closeTab(self, index):
        if self.tabWidget.count() > 1:
            self.tabWidget.removeTab(index)
