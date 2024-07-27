import logging
import os

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QDockWidget,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ..framework.fileTree import FileTree
from ..scripts.color_scheme_loader import color_schemes


class DockedFileTreeWidget(QWidget):
    def __init__(
        self,
        fileTree,
        currentDirLabel,
        fullPathLabel,
        explorerLabel,
        hideButton,
        parent=None,
    ):
        super().__init__(parent)
        logging.info("Initializing DockedFileTreeWidget")
        layout = QVBoxLayout(self)
        headerLayout = QHBoxLayout()
        headerLayout.addWidget(explorerLabel)
        headerLayout.addWidget(hideButton)
        layout.addLayout(headerLayout)

        layout.addWidget(currentDirLabel)
        layout.addWidget(fileTree)
        layout.addWidget(fullPathLabel)
        self.setLayout(layout)
        logging.info("DockedFileTreeWidget initialized")


class FileTreeWidget(QWidget):
    visibilityChanged = pyqtSignal(bool)
    dockingChanged = pyqtSignal(bool)

    def __init__(self, parent=None, zenithInstance=None):
        super().__init__(parent)
        self.initUI()

        self.isFloating = False
        zenithInstance.folderOpened.connect(self.updateLabels)

    def updateLabels(self, folderPath):
        self.currentDirLabel.setText(os.path.basename(folderPath))
        self.fullPathLabel.setText(folderPath)

    def setRootFolder(self, folderPath):
        self.fileTree.setRootFolder(folderPath)

    def initUI(self):
        fileTreeLayout = QVBoxLayout(self)
        headerLayout = QHBoxLayout()
        self.explorerLabel = QLabel("EXPLORER")
        fileTreeLayout.addWidget(self.explorerLabel)
        self.explorerLabel.setStyleSheet(
            f"""
            QLabel {{
                background-color: {color_schemes['sidebar_bg']};
                color: {color_schemes['sidebar_fg']};
                padding: 2px;
                border-top-left-radius: 4px;
            }}
            """
        )
        button_style = f"""
            background-color: {color_schemes['sidebar_button']};
            color: {color_schemes['sidebar_fg']};
            border: none;
        """
        self.hideButton = QPushButton("🗙")
        self.hideButton.setStyleSheet(button_style + "border-top-right-radius: 4px;")
        self.hideButton.setFixedSize(20, 20)
        self.hideButton.clicked.connect(self.toggleFileTreeVisibility)

        self.floatButton = QPushButton("🗗")
        self.floatButton.setStyleSheet(button_style + "border-bottom-left-radius: 4px;")
        self.floatButton.setFixedSize(20, 20)
        self.floatButton.clicked.connect(self.makeFileTreeFloat)

        # Button Positioning
        headerLayout.addWidget(self.explorerLabel)
        headerLayout.addWidget(self.floatButton)
        headerLayout.addWidget(self.hideButton)
        fileTreeLayout.addLayout(headerLayout)

        label_style = f"""
            background-color: {color_schemes['sidebar_bg']};
            color: {color_schemes['sidebar_fg']};
            padding: 2px;
        """

        self.currentDirLabel = QLabel(os.path.basename(os.getcwd()))
        self.currentDirLabel.setStyleSheet(label_style + "font-weight: bold;")

        self.fileTree = FileTree(self)
        fileTreeLayout.addWidget(self.currentDirLabel)
        fileTreeLayout.addWidget(self.fileTree)
        self.fullPathLabel = QLabel(os.getcwd())
        self.fullPathLabel.setStyleSheet(label_style + "font-style: italic;")
        fileTreeLayout.addWidget(self.fullPathLabel)
        fileTreeLayout.setContentsMargins(0, 0, 0, 0)
        fileTreeLayout.setSpacing(0)

    def toggleFileTreeVisibility(self):
        isVisible = not self.fileTree.isVisible()
        self.fileTree.setVisible(isVisible)
        self.explorerLabel.setVisible(isVisible)
        self.currentDirLabel.setVisible(isVisible)
        self.fullPathLabel.setVisible(isVisible)
        self.hideButton.setVisible(isVisible)

        self.visibilityChanged.emit(isVisible)

    def makeFileTreeFloat(self):
        if not hasattr(self, "floatingWidget") or not self.floatingWidget:
            dockedWidget = DockedFileTreeWidget(
                self.fileTree,
                self.currentDirLabel,
                self.fullPathLabel,
                self.explorerLabel,
                self.hideButton,
                self,
            )
            self.floatingWidget = QDockWidget("File Tree", self)
            self.floatingWidget.setWidget(dockedWidget)
            self.floatingWidget.setFloating(True)
            self.floatingWidget.show()
        else:
            self.floatingWidget.setVisible(not self.floatingWidget.isVisible())

        self.isFloating = not self.isFloating

        self.dockingChanged.emit(self.isFloating)
