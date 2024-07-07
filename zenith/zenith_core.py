from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QMainWindow,
    QSplitter,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from .framework.fileTree import FileTree
from .framework.statusBar import ZenithStatusBar
from .framework.titleBar import CustomTitleBar
from .scripts.def_path import resource


class Zenith(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowTitle("Zenith")
        self.setGeometry(100, 100, 800, 600)

        self.setWindowIcon(QIcon(resource("..\\media\\icon.ico")))

        self.titleBar = CustomTitleBar(self)  # Title bar
        self.setMenuWidget(self.titleBar)

        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        layout = QVBoxLayout(centralWidget)

        splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(splitter)

        self.tabWidget = QTabWidget()
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.tabCloseRequested.connect(self.closeTab)
        splitter.addWidget(self.tabWidget)

        self.addNewTab()  # Add the initial tab
        newTabShortcut = QShortcut(QKeySequence("Ctrl+T"), self)
        newTabShortcut.activated.connect(self.addNewTab)

        self.fileTree = FileTree(self)
        splitter.addWidget(self.fileTree)

        self.statusBar = ZenithStatusBar(self, self)
        self.setStatusBar(self.statusBar)

        splitter.setSizes([600, 150])

    def addNewTab(self, content=""):
        newTab = QTextEdit()
        if isinstance(content, str):
            newTab.setText(content)
        else:
            newTab.setText("")
        tabIndex = self.tabWidget.addTab(newTab, "Document")
        self.tabWidget.setCurrentIndex(tabIndex)

    def closeTab(self, index):
        if self.tabWidget.count() > 1:
            self.tabWidget.removeTab(index)
