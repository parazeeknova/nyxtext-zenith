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
                font-style: italic;
                font-weight: bold;
                margin-bottom: 4px;
                border-bottom-left-radius: 4px;
                border-bottom-right-radius: 4px;
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
                margin-top: 4px;
                border-radius: 4px;
                font-style: italic;
            }
        """
        )
        fileTreeLayout.addWidget(fullPathLabel)
        fileTreeLayout.setContentsMargins(0, 0, 0, 0)
        fileTreeLayout.setSpacing(0)
