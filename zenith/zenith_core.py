from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QSplitter, QTextEdit, QVBoxLayout, QWidget

from .components.rightSideBar import FileTreeWidget
from .components.tabTopbar import tabRow
from .framework.statusBar import ZenithStatusBar
from .framework.titleBar import CustomTitleBar
from .scripts.def_path import resource
from .scripts.shortcuts import key_shortcuts


class Zenith(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setWindowTitle("Zenith")
        self.setGeometry(100, 100, 800, 600)

        self.setWindowIcon(QIcon(resource(r"../media/icon.ico")))

        self.titleBar = CustomTitleBar(self)  # Title bar or the top bar
        self.setMenuWidget(self.titleBar)

        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        layout = QVBoxLayout(centralWidget)

        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        layout.addWidget(self.splitter)

        tabRow(self, self.splitter)  # Tab row or the top bar

        self.fileTree = FileTreeWidget()
        self.splitter.addWidget(self.fileTree)

        self.fileTree.visibilityChanged.connect(self.adjustSplitter)
        self.fileTree.dockingChanged.connect(self.handleDockingChange)

        self.statusBar = ZenithStatusBar(self, self)  # Status bar or the bottom bar
        self.setStatusBar(self.statusBar)

        key_shortcuts(self)  # Keyboard shortcuts defined in shortcuts.json
        self.splitter.setSizes([600, 150])  # Set the initial size of the splitter panes

        self.setDockNestingEnabled(True)
        self.setDockOptions(
            QMainWindow.DockOption.AnimatedDocks
            | QMainWindow.DockOption.AllowNestedDocks
        )

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

    def adjustSplitter(self, isVisible):
        if isVisible:
            self.splitter.setSizes([600, 150])
        else:
            self.splitter.setSizes([750, 0])

    def handleDockingChange(self, isDocked):
        if isDocked:
            self.splitter.setSizes([750, 0])
        else:
            self.splitter.setSizes([600, 150])
