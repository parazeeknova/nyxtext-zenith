import os

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QDockWidget,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ..framework.fileTree import FileTree


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
        layout = QVBoxLayout(self)
        headerLayout = QHBoxLayout()
        headerLayout.addWidget(explorerLabel)
        headerLayout.addWidget(hideButton)
        layout.addLayout(headerLayout)

        layout.addWidget(currentDirLabel)
        layout.addWidget(fileTree)
        layout.addWidget(fullPathLabel)
        self.setLayout(layout)


class FileTreeWidget(QWidget):
    visibilityChanged = Signal(bool)
    dockingChanged = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

        self.isFloating = False

    def initUI(self):
        fileTreeLayout = QVBoxLayout(self)
        headerLayout = QHBoxLayout()
        self.explorerLabel = QLabel("EXPLORER")
        fileTreeLayout.addWidget(self.explorerLabel)
        self.explorerLabel.setStyleSheet(
            """
            QLabel {
                background-color: #333;
                color: #fff;
                padding: 2px;
                border-top-left-radius: 4px;
            }
        """
        )

        self.hideButton = QPushButton("🗙")
        self.hideButton.setStyleSheet(
            """
            background-color: #333;
            color: #fff; border: none;
            border-top-right-radius: 4px;
            """
        )
        self.hideButton.setFixedSize(20, 20)
        self.hideButton.clicked.connect(self.toggleFileTreeVisibility)

        self.floatButton = QPushButton("🗗")
        self.floatButton.setStyleSheet(
            "background-color: #333; color: #fff; border: none;"
        )
        self.floatButton.setFixedSize(20, 20)
        self.floatButton.clicked.connect(self.makeFileTreeFloat)

        # Button Positioning
        headerLayout.addWidget(self.explorerLabel)
        headerLayout.addWidget(self.floatButton)
        headerLayout.addWidget(self.hideButton)
        fileTreeLayout.addLayout(headerLayout)

        self.currentDirLabel = QLabel(os.path.basename(os.getcwd()))

        self.currentDirLabel.setStyleSheet(
            """
            QLabel {
                background-color: #333;
                color: #aaa; padding: 2px;
                font-weight: bold;
                margin-bottom: 0px;
                border-bottom-left-radius: 0px;
                border-bottom-right-radius: 0px;
                padding: 2px;
            }
        """
        )

        self.fileTree = FileTree(self)
        fileTreeLayout.addWidget(self.currentDirLabel)
        fileTreeLayout.addWidget(self.fileTree)
        self.fullPathLabel = QLabel(os.getcwd())

        self.fullPathLabel.setStyleSheet(
            """
            QLabel {
                background-color: #333;
                color: #fff;
                padding: 4px;
                margin-top: 0px;
                font-style: italic;
                border-top-left-radius: 0px;
                border-top-right-radius: 0px;
                border-bottom-left-radius: 4px;
                border-bottom-right-radius: 4px;
            }
        """
        )
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
