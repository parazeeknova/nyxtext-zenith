import logging
import os

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QIcon
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
from ..scripts.def_path import resource

newFolderIcon = resource(r"../media/filetree_toolkit/folder.svg")
newFileIcon = resource(r"../media/filetree_toolkit/file.svg")
dockIcon = resource(r"../media/filetree_toolkit/dock.svg")
hideIcon = resource(r"../media/filetree_toolkit/hide.svg")


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
                border-top-right-radius: 4px;
            }}
            """
        )
        button_style = f"""
            background-color: {color_schemes['sidebar_button']};
            color: {color_schemes['sidebar_fg']};
            border: none;
            padding: 2px;
            spacing: 2px;
        """
        self.hideButton = QPushButton()
        self.hideButton.setIcon(QIcon(hideIcon))
        self.hideButton.setStyleSheet(button_style + "border-top-right-radius: 4px;")
        self.hideButton.setFixedSize(20, 20)
        self.hideButton.clicked.connect(self.toggleFileTreeVisibility)

        self.floatButton = QPushButton()
        self.floatButton.setIcon(QIcon(dockIcon))
        self.floatButton.setStyleSheet(button_style)
        self.floatButton.setFixedSize(20, 20)
        self.floatButton.clicked.connect(self.makeFileTreeFloat)

        self.newFileButton = QPushButton()
        self.newFileButton.setIcon(QIcon(newFileIcon))
        self.newFileButton.setStyleSheet(button_style + "border-top-left-radius: 4px;")
        self.newFileButton.setFixedSize(20, 20)
        self.newFileButton.clicked.connect(self.createNewFile)

        self.newFolderButton = QPushButton()
        self.newFolderButton.setIcon(QIcon(newFolderIcon))
        self.newFolderButton.setStyleSheet(button_style)
        self.newFolderButton.setFixedSize(20, 20)
        self.newFolderButton.clicked.connect(self.createNewFolder)

        # Button Positioning
        headerLayout.addWidget(self.explorerLabel)
        headerLayout.addStretch()
        headerLayout.addWidget(self.newFileButton)
        headerLayout.addWidget(self.newFolderButton)
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

        self.fileTree = FileTree(self, fileTreeWidget=self)
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

    def createNewFile(self):
        parent_index = self.fileTree.currentIndex()
        parent_path = self.fileTree.model.filePath(parent_index)
        if not os.path.isdir(parent_path):
            parent_path = os.path.dirname(parent_path)

        new_file_path = os.path.join(parent_path, "Untitled")
        counter = 1
        while os.path.exists(new_file_path):
            new_file_path = os.path.join(parent_path, f"Untitled{counter}")
            counter += 1

        with open(new_file_path, "w") as f:
            pass

        new_index = self.fileTree.model.index(new_file_path)
        self.fileTree.setCurrentIndex(new_index)
        self.fileTree.edit(new_index)

    def createNewFolder(self):
        parent_index = self.fileTree.currentIndex()
        parent_path = self.fileTree.model.filePath(parent_index)
        if not os.path.isdir(parent_path):
            parent_path = os.path.dirname(parent_path)

        new_folder_path = os.path.join(parent_path, "New Folder")
        counter = 1
        while os.path.exists(new_folder_path):
            new_folder_path = os.path.join(parent_path, f"New Folder {counter}")
            counter += 1

        os.mkdir(new_folder_path)

        new_index = self.fileTree.model.index(new_folder_path)
        self.fileTree.setCurrentIndex(new_index)
        self.fileTree.edit(new_index)
