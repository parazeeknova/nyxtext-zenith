import os

from PyQt6.QtCore import QDir, QEasingCurve, QPropertyAnimation, Qt, pyqtSignal
from PyQt6.QtGui import QAction, QColor, QIcon, QPainter
from PyQt6.QtWidgets import (
    QGraphicsOpacityEffect,
    QInputDialog,
    QMenu,
    QMessageBox,
    QTreeView,
)

from ..core.customFileSystemModel import CustomFileSystemModel
from ..scripts.color_scheme_loader import color_schemes
from ..scripts.def_path import resource

renameIcon = resource(r"../media/context_menu/rename.svg")
deleteIcon = resource(r"../media/context_menu/trash.svg")
newFileIcon = resource(r"../media/context_menu/new_file.svg")
newFolderIcon = resource(r"../media/context_menu/new_folder.svg")
hideIcon = resource(r"../media/context_menu/hide_filetree.svg")
dockIcon = resource(r"../media/context_menu/dock.svg")
refreshIcon = resource(r"../media/context_menu/refresh.svg")


class CustomMenu(QMenu):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(
            f"""
            QMenu {{
                background-color: {color_schemes['menu_bg']};
                color: {color_schemes['menu_fg']};
                border: 1px solid {color_schemes['menu_separator']};
                border-radius: 5px;
                padding: 2px;
            }}
            QMenu::item {{
                padding: 5px 10px 5px 10px;
                border-radius: 3px;
            }}
            QMenu::item:selected {{
                background-color: {color_schemes['menu_selected']};
            }}
            QMenu::separator {{
                height: 1px;
                background-color: {color_schemes['menu_separator']};
                margin: 5px 0px 5px 0px;
            }}
        """
        )

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(color_schemes["menu_bg"]))
        painter.drawRoundedRect(self.rect(), 5, 5)
        super().paintEvent(event)


class FileTree(QTreeView):
    fileSelected = pyqtSignal(str)

    def __init__(self, parent=None, fileTreeWidget=None):
        super().__init__(parent)

        self.fileTreeWidget = fileTreeWidget
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

        self.setEditTriggers(QTreeView.EditTrigger.NoEditTriggers)
        self.doubleClicked.connect(self.onDoubleClick)

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)

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

    def onDoubleClick(self, index):
        if self.model.isDir(index):
            # Expand or collapse the directory
            if self.isExpanded(index):
                self.collapse(index)
            else:
                self.expand(index)
        else:
            # For files, emit the fileSelected signal
            self.onFileSelected(index)

    def edit(self, index, trigger=QTreeView.EditTrigger.NoEditTriggers, event=None):
        if not self.model.isDir(index):
            return super().edit(index, trigger, event)
        return False

    def showContextMenu(self, point):
        index = self.indexAt(point)
        menu = CustomMenu(self)

        if index.isValid():
            # Context menu for files/folders
            rename_action = QAction("Rename", self)
            delete_action = QAction("Delete", self)

            rename_icon = QIcon(renameIcon)
            delete_icon = QIcon(deleteIcon)

            rename_action.setIcon(rename_icon)
            delete_action.setIcon(delete_icon)

            rename_action.triggered.connect(lambda: self.renameItem(index))
            delete_action.triggered.connect(lambda: self.deleteItem(index))

            menu.addAction(rename_action)
            menu.addAction(delete_action)
        else:
            # Context menu for blank space
            new_file_action = QAction("New File", self)
            new_folder_action = QAction("New Folder", self)
            hide_action = QAction("Hide File Tree", self)
            dock_action = QAction("Dock/Undock File Tree", self)
            refresh_action = QAction("Refresh", self)

            new_file_icon = QIcon(newFileIcon)
            new_folder_icon = QIcon(newFolderIcon)
            hide_icon = QIcon(hideIcon)
            dock_icon = QIcon(dockIcon)
            refresh_icon = QIcon(refreshIcon)

            new_file_action.setIcon(new_file_icon)
            new_folder_action.setIcon(new_folder_icon)
            hide_action.setIcon(hide_icon)
            dock_action.setIcon(dock_icon)
            refresh_action.setIcon(refresh_icon)

            new_file_action.triggered.connect(self.fileTreeWidget.createNewFile)
            new_folder_action.triggered.connect(self.fileTreeWidget.createNewFolder)
            hide_action.triggered.connect(self.fileTreeWidget.toggleFileTreeVisibility)
            dock_action.triggered.connect(self.fileTreeWidget.makeFileTreeFloat)
            refresh_action.triggered.connect(self.refreshFileTree)

            menu.addAction(new_file_action)
            menu.addAction(new_folder_action)
            menu.addSeparator()
            menu.addAction(hide_action)
            menu.addAction(dock_action)
            menu.addSeparator()
            menu.addAction(refresh_action)

        menu.exec(self.viewport().mapToGlobal(point))

    def refreshFileTree(self):
        self.model.setRootPath(self.model.rootPath())

    def renameItem(self, index):
        old_name = self.model.fileName(index)
        file_path = self.model.filePath(index)
        parent_path = os.path.dirname(file_path)

        new_name, ok = QInputDialog.getText(
            self, "Rename", "Enter new name:", text=old_name
        )

        if ok and new_name and new_name != old_name:
            new_path = os.path.join(parent_path, new_name)
            try:
                os.rename(file_path, new_path)
                self.model.setData(index, new_name, Qt.ItemDataRole.EditRole)
            except OSError as e:
                QMessageBox.critical(
                    self, "Error", f"Could not rename {old_name}: {str(e)}"
                )

    def deleteItem(self, index):
        file_path = self.model.filePath(index)
        file_name = os.path.basename(file_path)

        reply = QMessageBox.question(
            self,
            "Delete Confirmation",
            f"Are you sure you want to delete '{file_name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                if os.path.isdir(file_path):
                    os.rmdir(file_path)
                else:
                    os.remove(file_path)
                self.model.remove(index)
            except OSError as e:
                QMessageBox.critical(
                    self, "Error", f"Could not delete {file_name}: {str(e)}"
                )
