import os

from PyQt6.Qsci import QsciScintilla
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QFileDialog,
    QMainWindow,
    QMessageBox,
    QSplitter,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from .components.codeSpace import Codespace
from .components.rightSideBar import FileTreeWidget
from .components.tabTopbar import tabRow
from .components.workSpace import Workspace
from .framework.lexer_manager import LexerManager
from .framework.statusBar import ZenithStatusBar
from .framework.titleBar import CustomTitleBar
from .scripts.def_path import resource
from .scripts.shortcuts import key_shortcuts


class Zenith(QMainWindow):
    folderOpened = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.lexerManager = LexerManager()

        self.tabCounter = 0
        self.filePathDict = {}

        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setWindowTitle("Zenith")
        self.setGeometry(100, 100, 800, 600)

        self.setWindowIcon(QIcon(resource(r"../media/icon.ico")))

        self.titleBar = CustomTitleBar(self, self)  # Title bar or the top bar
        self.setMenuWidget(self.titleBar)

        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        layout = QVBoxLayout(centralWidget)

        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        layout.addWidget(self.splitter)

        tabRow(self, self.splitter)  # Tab row or the top bar

        self.fileTree = FileTreeWidget(self, self)
        self.splitter.addWidget(self.fileTree)

        self.fileTree.visibilityChanged.connect(self.adjustSplitter)
        self.fileTree.dockingChanged.connect(self.handleDockingChange)
        self.tabWidget.currentChanged.connect(self.onTabChange)
        self.fileTree.fileTree.fileSelected.connect(self.openFileFromTree)
        self.tabWidget.tabCloseRequested.connect(self.handleTabClose)

        self.statusBar = ZenithStatusBar(self)  # Status bar or the bottom bar
        self.setStatusBar(self.statusBar)

        key_shortcuts(self)  # Keyboard shortcuts defined in shortcuts.json
        self.splitter.setSizes([600, 150])  # Set the initial size of the splitter panes

        self.setDockNestingEnabled(True)
        self.setDockOptions(
            QMainWindow.DockOption.AnimatedDocks
            | QMainWindow.DockOption.AllowNestedDocks
        )

        self.codespace = Codespace(self.tabWidget)

        self.codespace.cursorPositionChanged.connect(self.handleCursorPositionChanged)

        self.lexerManager = LexerManager()

    def handleCursorPositionChanged(self):
        self.updateStatusBar()

    def addNewTab(self):
        Workspace(self)

    def closeTab(self, index):
        if self.tabWidget.count() > 1:
            self.tabWidget.widget(index)
            if self.isModified():
                reply = QMessageBox.question(
                    self,
                    "Save Changes?",
                    "Do you want to save changes before closing?",
                    QMessageBox.StandardButton.Yes
                    | QMessageBox.StandardButton.No
                    | QMessageBox.StandardButton.Cancel,
                )
                if reply == QMessageBox.StandardButton.Yes:
                    self.saveFile()
                elif reply == QMessageBox.StandardButton.Cancel:
                    return

            self.tabWidget.removeTab(index)
            if index in self.filePathDict:
                del self.filePathDict[index]
            updatedFilePathDict = {}
            for tabIndex, filePath in self.filePathDict.items():
                if tabIndex > index:
                    updatedFilePathDict[tabIndex - 1] = filePath
                else:
                    updatedFilePathDict[tabIndex] = filePath
            self.filePathDict = updatedFilePathDict
        if self.tabWidget.count() == 0:
            self.titleBar.updateTitle(None)

    def adjustSplitter(self, isVisible):
        if isVisible:
            self.splitter.setSizes([600, 150])
        else:
            self.splitter.setSizes([750, 0])

    def handleDockingChange(self, isDocked):
        if isDocked:
            self.splitter.setSizes([750, 0])
        else:
            self.splitter.setSizes([600, 150])

    def centralizedOpenFile(self, filePath):
        for tabIndex, openFilePath in self.filePathDict.items():
            if openFilePath == filePath:
                self.tabWidget.setCurrentIndex(tabIndex)
                return
        self.actualOpenFile(filePath)

    def actualOpenFile(self, filePath):
        fileName = os.path.basename(filePath)
        folderName = os.path.basename(os.path.dirname(filePath))
        self.statusBar.showLexerLoadingMessage()
        self.titleBar.updateTitle(folderName, fileName)
        with open(filePath, "r", encoding="utf-8") as file:
            content = file.read()
            if filePath.endswith(".txt"):
                tabIndex = self.tabWidget.addTab(
                    Workspace(self, content, fileName=fileName), fileName
                )
            else:
                tabIndex = self.tabWidget.addTab(
                    Codespace(self.tabWidget, content, file_path=filePath), fileName
                )
            self.tabWidget.setTabText(tabIndex, fileName)
            self.filePathDict[tabIndex] = filePath

    def openFile(self):
        filePath, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", "All Files (*)"
        )
        if filePath:
            self.centralizedOpenFile(filePath)
            self.statusBar.showMessage(f"Opened file: {filePath}", 4000)

    def openFileFromTree(self, filePath):
        self.centralizedOpenFile(filePath)
        self.updateStatusBarWithLexer()

    def onTabChange(self, index):
        filePath = self.retrieveFilePathForTab(index)
        self.updateStatusBarWithLexer()
        if filePath:
            folderName = os.path.basename(os.path.dirname(filePath))
            fileName = os.path.basename(filePath)
            self.titleBar.updateTitle(folderName, fileName)
        else:
            self.titleBar.updateTitle(None, "Untitled")

    def retrieveFilePathForTab(self, index):
        return self.filePathDict.get(index, None)

    def nextTab(self):
        currentIndex = self.tabWidget.currentIndex()
        if currentIndex < self.tabWidget.count() - 1:
            self.tabWidget.setCurrentIndex(currentIndex + 1)
        else:
            self.tabWidget.setCurrentIndex(0)

    def prevTab(self):
        currentIndex = self.tabWidget.currentIndex()
        if currentIndex > 0:
            self.tabWidget.setCurrentIndex(currentIndex - 1)
        else:
            self.tabWidget.setCurrentIndex(self.tabWidget.count() - 1)

    def closeAllTabs(self):
        for index in range(self.tabWidget.count() - 1, -1, -1):
            self.closeTab(index)

    def handleTabClose(self, index):
        if index in self.filePathDict:
            del self.filePathDict[index]
        self.tabWidget.removeTab(index)
        newFilePathDict = {}
        for tabIndex in range(self.tabWidget.count()):
            widget = self.tabWidget.widget(tabIndex)
            if hasattr(widget, "fileName"):
                filePath = self.filePathDict.get(tabIndex)
                if filePath:
                    newFilePathDict[tabIndex] = filePath
        self.filePathDict = newFilePathDict

    def saveFile(self):
        currentIndex = self.tabWidget.currentIndex()
        filePath = self.retrieveFilePathForTab(currentIndex)
        if filePath:
            currentWidget = self.tabWidget.currentWidget()
            if isinstance(currentWidget, QsciScintilla):
                content = currentWidget.text()
                with open(filePath, "w") as file:
                    file.write(content)
                self.removeUnsavedChangesMarker(currentWidget)
            elif isinstance(currentWidget, QTextEdit):
                content = currentWidget.toPlainText()
                with open(filePath, "w") as file:
                    file.write(content)
            print(f"File saved: {filePath}")
            self.statusBar.showMessage(
                f"File saved in {os.path.dirname(filePath)}", 4000
            )
        else:
            self.saveFileAs()

    def saveFileAs(self):
        filePath, _ = QFileDialog.getSaveFileName(
            self, "Save File", "", "All Files (*)"
        )
        if filePath:
            currentIndex = self.tabWidget.currentIndex()
            currentWidget = self.tabWidget.currentWidget()
            if isinstance(currentWidget, QsciScintilla):
                content = currentWidget.text()
            elif isinstance(currentWidget, QTextEdit):
                content = currentWidget.toPlainText()
            with open(filePath, "w") as file:
                file.write(content)
            self.filePathDict[currentIndex] = filePath
            fileName = os.path.basename(filePath)
            self.tabWidget.setTabText(currentIndex, fileName)
            self.removeUnsavedChangesMarker(currentWidget)
            print(f"File saved as: {filePath}")

    def removeUnsavedChangesMarker(self, codespace):
        UNSAVED_CHANGES_MARKER_NUM = 9
        codespace.markerDeleteAll(UNSAVED_CHANGES_MARKER_NUM)

    def isModified(self):
        currentWidget = self.tabWidget.currentWidget()
        if isinstance(currentWidget, QsciScintilla):
            return currentWidget.isModified()
        elif isinstance(currentWidget, QTextEdit):
            return currentWidget.document().isModified()
        return False

    def openFolder(self):
        folderPath = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folderPath:
            self.fileTree.setRootFolder(folderPath)
            self.folderOpened.emit(folderPath)

    def updateStatusBar(self):
        sender = self.sender()
        if isinstance(sender, QTextEdit):
            cursor = sender.textCursor()
            lineNumber = cursor.blockNumber() + 1
            columnNumber = cursor.columnNumber() + 1
            totalLines = sender.document().blockCount()
            words = len(sender.toPlainText().split())
        elif isinstance(sender, QsciScintilla):
            lineNumber, columnNumber = sender.getCursorPosition()
            lineNumber += 1
            columnNumber += 1
            totalLines = sender.lines()
            words = len(sender.text().split())
        else:
            return  # Unknown sender

        self.statusBar.updateStats(lineNumber, columnNumber, totalLines, words)

    def updateStatusBarWithLexer(self):
        currentWidget = self.tabWidget.currentWidget()
        if currentWidget:
            filePath = self.filePathDict.get(self.tabWidget.currentIndex())
            if filePath:
                fileExtension = filePath.split(".")[-1]
                lexer = self.lexerManager.get_lexer(fileExtension)
                if lexer:
                    lexerName = type(lexer).__name__
                    self.statusBar.updateLexer(lexerName)
                else:
                    self.statusBar.updateLexer("None")
            else:
                self.statusBar.updateLexer("None")
        else:
            self.statusBar.updateLexer("None")
