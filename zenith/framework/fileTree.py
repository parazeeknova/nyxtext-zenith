import os

from PyQt6.QtCore import QDir
from PyQt6.QtGui import QFileSystemModel
from PyQt6.QtWidgets import QTreeView


class FileTree(QTreeView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.model = QFileSystemModel()
        self.model.setFilter(
            QDir.Filter.Files | QDir.Filter.Dirs | QDir.Filter.NoDotAndDotDot
        )
        self.model.setRootPath(os.getcwd())
        self.setModel(self.model)
        self.setRootIndex(self.model.index(os.getcwd()))
        self.setHeaderHidden(True)

        for column in range(1, self.model.columnCount()):
            self.hideColumn(column)

        self.setStyleSheet(
            """
            QTreeView {
                border-radius: 0px;
            }
        """
        )
