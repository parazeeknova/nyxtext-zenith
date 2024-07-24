import os

from PyQt6.QtCore import QDir, QPropertyAnimation, pyqtSignal, QEasingCurve
from PyQt6.QtWidgets import QGraphicsOpacityEffect, QTreeView

from ..core.customFileSystemModel import CustomFileSystemModel
from ..scripts.color_scheme_loader import color_schemes


class FileTree(QTreeView):
    fileSelected = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.doubleClicked.connect(self.onFileSelected)
        self.model = CustomFileSystemModel(self)
        self.model.setFilter(
            QDir.Filter.Files | QDir.Filter.Dirs | QDir.Filter.NoDotAndDotDot
        )
        self.model.setRootPath(os.getcwd())
        self.setModel(self.model)
        self.setRootIndex(self.model.index(os.getcwd()))
        self.setHeaderHidden(True)

        self.opacity_effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(0)

        self.fade_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_animation.setDuration(500)
        self.fade_animation.setStartValue(0)
        self.fade_animation.setEndValue(1)
        self.fade_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)

        for column in range(1, self.model.columnCount()):
            self.hideColumn(column)

        self.setStyleSheet(
            f"""
            QTreeView {{
                background-color: {color_schemes['filetree_bg']};
                color: {color_schemes['filetree_fg']};
                border-radius: 0px;
            }}
            QTreeView::item:selected {{
                background-color: {color_schemes['filetree_selected']};
            }}
            QTreeView::item:hover {{
                background-color: {color_schemes['filetree_hover']};
            }}
            """
        )

    def onFileSelected(self, index):
        filePath = self.model.filePath(index)
        self.fileSelected.emit(filePath)

    def setRootFolder(self, folderPath):
        self.model.setRootPath(folderPath)
        self.setRootIndex(self.model.index(folderPath))

    def showEvent(self, event):
        super().showEvent(event)
        self.fade_animation.start()
