import os

from PySide6.QtCore import QDir
from PySide6.QtWidgets import QFileSystemModel, QTreeView


class FileTree(QTreeView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.model = QFileSystemModel()
        self.model.setFilter(QDir.Files | QDir.Dirs | QDir.NoDotAndDotDot)
        self.model.setRootPath(os.getcwd())
        self.setModel(self.model)
        self.setRootIndex(self.model.index(os.getcwd()))
        self.setHeaderHidden(True)

        for column in range(1, self.model.columnCount()):
            self.hideColumn(column)
