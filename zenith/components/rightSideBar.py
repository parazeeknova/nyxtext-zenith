import os

from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from ..framework.fileTree import FileTree


class FileTreeWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        fileTreeLayout = QVBoxLayout(self)
        explorerLabel = QLabel("EXPLORER")
        fileTreeLayout.addWidget(explorerLabel)
        explorerLabel.setStyleSheet(
            """
            QLabel {
                background-color: #333;
                color: #fff;
                padding: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
        """
        )
        currentDirLabel = QLabel(os.path.basename(os.getcwd()))
        currentDirLabel.setStyleSheet(
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
        fileTreeLayout.addWidget(currentDirLabel)
        fileTree = FileTree(self)
        fileTreeLayout.addWidget(fileTree)
        fullPathLabel = QLabel(os.getcwd())
        fullPathLabel.setStyleSheet(
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
        fileTreeLayout.addWidget(fullPathLabel)
        fileTreeLayout.setContentsMargins(0, 0, 0, 0)
        fileTreeLayout.setSpacing(0)
