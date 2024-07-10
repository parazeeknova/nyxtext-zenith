import os

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QFileDialog, QMainWindow, QSplitter, QVBoxLayout, QWidget

from .components.codeSpace import Codespace
from .components.rightSideBar import FileTreeWidget
from .components.tabTopbar import tabRow
from .components.workSpace import Workspace
from .framework.statusBar import ZenithStatusBar
from .framework.titleBar import CustomTitleBar
from .scripts.def_path import resource
from .scripts.shortcuts import key_shortcuts


class Zenith(QMainWindow):
    def __init__(self):
        super().__init__()

        self.tabCounter = 0

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

        Codespace(self.tabWidget)
        Workspace(self)

    def addNewTab(self):
        Workspace(self)

    def closeTab(self, index):
        if self.tabWidget.count() > 1:
            self.tabWidget.removeTab(index)

    def removeCurrentCodespace(self):
        currentIndex = self.tabWidget.currentIndex()
        if currentIndex != -1:
            self.tabWidget.removeTab(currentIndex)

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

    def openFile(self):
        filePath, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", "All Files (*)"
        )
        if filePath:
            fileName = os.path.basename(filePath)
            if filePath.endswith(".txt"):
                with open(filePath, "r") as file:
                    content = file.read()
                    Workspace(self, content)
                    self.tabWidget.setTabText(self.tabWidget.currentIndex(), fileName)
            else:
                with open(filePath, "r") as file:
                    content = file.read()
                Codespace(self.tabWidget, content)
                self.tabWidget.setTabText(self.tabWidget.currentIndex(), fileName)
