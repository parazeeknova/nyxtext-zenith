import os

import chardet
from PyQt6.Qsci import QsciScintilla
from PyQt6.QtCore import QObject, QRunnable, Qt, QThreadPool, pyqtSignal
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QApplication,
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
from .scripts.file_cache import FileCache
from .scripts.shortcuts import key_shortcuts


class FileWorker(QRunnable):
    class Signals(QObject):
        finished = pyqtSignal(str, str)
        error = pyqtSignal(str)

    def __init__(self, file_path, content=None, mode="r"):
        super().__init__()
        self.file_path = file_path
        self.content = content
        self.mode = mode
        self.signals = self.Signals()

    def run(self):
        try:
            if self.mode == "r":
                with open(self.file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                self.signals.finished.emit(self.file_path, content)
            elif self.mode == "w":
                with open(self.file_path, "w", encoding="utf-8") as file:
                    file.write(self.content)
                self.signals.finished.emit(self.file_path, "")
        except Exception as e:
            self.signals.error.emit(str(e))


class Zenith(QMainWindow):
    folderOpened = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.threadPool = QThreadPool()
        self.lexerManager = LexerManager()
        self.filePathDict = {}
        self.fileCache = FileCache()
        self.tabCounter = 0

        self.setupUI()
        self.setupConnections()

    def setupUI(self):
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setWindowTitle("Zenith")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon(resource(r"../media/icon.ico")))

        self.titleBar = CustomTitleBar(self, self)
        self.setMenuWidget(self.titleBar)

        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        layout = QVBoxLayout(centralWidget)

        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        layout.addWidget(self.splitter)

        tabRow(self, self.splitter)

        self.fileTree = FileTreeWidget(self, self)
        self.splitter.addWidget(self.fileTree)

        self.statusBar = ZenithStatusBar(self)
        self.setStatusBar(self.statusBar)

        key_shortcuts(self)
        self.splitter.setSizes([600, 150])

        self.setDockNestingEnabled(True)
        self.setDockOptions(
            QMainWindow.DockOption.AnimatedDocks
            | QMainWindow.DockOption.AllowNestedDocks
        )

        self.codespace = Codespace(self.tabWidget)

    def setupConnections(self):
        self.fileTree.visibilityChanged.connect(self.adjustSplitter)
        self.fileTree.dockingChanged.connect(self.handleDockingChange)
        self.tabWidget.currentChanged.connect(self.onTabChange)
        self.fileTree.fileTree.fileSelected.connect(self.openFileFromTree)
        self.tabWidget.tabCloseRequested.connect(self.handleTabClose)
        self.codespace.cursorPositionChanged.connect(self.handleCursorPositionChanged)

    def closeApplication(self):
        self.closeAllTabs()
        self.fileCache.clear()
        QApplication.quit()

    def closeEvent(self, event):
        self.closeApplication()
        event.accept()

    def handleCursorPositionChanged(self):
        self.updateStatusBar()

    def addNewTab(self):
        Workspace(self)

    def closeTab(self, index):
        if self.tabWidget.count() > 1:
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
            self.updateFilePathDict()

        if self.tabWidget.count() == 0:
            self.titleBar.updateTitle(None)

    def updateFilePathDict(self):
        updatedFilePathDict = {}
        for tabIndex in range(self.tabWidget.count()):
            if tabIndex in self.filePathDict:
                updatedFilePathDict[tabIndex] = self.filePathDict[tabIndex]
        self.filePathDict = updatedFilePathDict

    def adjustSplitter(self, isVisible):
        self.splitter.setSizes([600, 150] if isVisible else [750, 0])

    def handleDockingChange(self, isDocked):
        self.splitter.setSizes([750, 0] if isDocked else [600, 150])

    def centralizedOpenFile(self, filePath):
        for tabIndex, openFilePath in self.filePathDict.items():
            if openFilePath == filePath:
                self.tabWidget.setCurrentIndex(tabIndex)
                return

        # Check if file is in cache
        cached_content = self.fileCache.get(filePath)
        if cached_content is not None:
            self.onFileOpenFinished(filePath, cached_content)
        else:
            worker = FileWorker(filePath)
            worker.signals.finished.connect(self.onFileOpenFinished)
            worker.signals.error.connect(
                lambda e: self.showErrorMessage("Error opening file", e)
            )
            self.threadPool.start(worker)

    def onFileOpenFinished(self, filePath, content):
        try:
            fileName = os.path.basename(filePath)
            folderName = os.path.basename(os.path.dirname(filePath))
            self.statusBar.showLexerLoadingMessage()
            self.titleBar.updateTitle(folderName, fileName)

            tab = (
                Workspace(self, content, fileName=fileName)
                if filePath.endswith(".txt")
                else Codespace(self.tabWidget, content, file_path=filePath)
            )

            tabIndex = self.tabWidget.addTab(tab, fileName)
            self.filePathDict[tabIndex] = filePath
            self.tabWidget.setCurrentIndex(tabIndex)
            self.statusBar.showMessage(f"Opened file: {filePath}", 4000)

            self.updateStatusBar()

            # Add file content to cache
            self.fileCache.set(filePath, content)
        except Exception as e:
            self.showErrorMessage("Error processing opened file", str(e))

    def showErrorMessage(self, title, message):
        QMessageBox.critical(self, title, message)

    def openFile(self):
        filePath, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", "All Files (*)"
        )
        if filePath:
            self.centralizedOpenFile(filePath)

    def openFileFromTree(self, filePath):
        self.centralizedOpenFile(filePath)
        currentWidget = self.tabWidget.currentWidget()
        if isinstance(currentWidget, QsciScintilla) and hasattr(
            currentWidget, "toggle_edit_mode"
        ):
            currentWidget.setReadOnly(True)
            currentWidget.markerDeleteAll(11)  # Delete edit mode marker
            currentWidget.markerAdd(0, 10)  # Add readonly marker
        self.updateStatusBarWithLexer()
        self.updateStatusBar()

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
        self.tabWidget.setCurrentIndex((currentIndex + 1) % self.tabWidget.count())

    def prevTab(self):
        currentIndex = self.tabWidget.currentIndex()
        self.tabWidget.setCurrentIndex((currentIndex - 1) % self.tabWidget.count())

    def closeAllTabs(self):
        for index in range(self.tabWidget.count() - 1, -1, -1):
            self.closeTab(index)

    def handleTabClose(self, index):
        if index in self.filePathDict:
            filePath = self.filePathDict[index]
            del self.filePathDict[index]
            # Remove file from cache when tab is closed
            self.fileCache.remove(filePath)
        self.tabWidget.removeTab(index)
        self.updateFilePathDict()

    def saveFile(self):
        currentIndex = self.tabWidget.currentIndex()
        filePath = self.retrieveFilePathForTab(currentIndex)
        if filePath:
            currentWidget = self.tabWidget.currentWidget()
            content = (
                currentWidget.text()
                if isinstance(currentWidget, QsciScintilla)
                else currentWidget.toPlainText()
            )

            worker = FileWorker(filePath, content, mode="w")
            worker.signals.finished.connect(self.onFileSaveFinished)
            worker.signals.error.connect(
                lambda e: self.showErrorMessage("Error saving file", e)
            )
            self.threadPool.start(worker)

            # Update cache with new content
            self.fileCache.set(filePath, content)
        else:
            self.saveFileAs()

    def onFileSaveFinished(self, filePath, _):
        self.removeUnsavedChangesMarker(self.tabWidget.currentWidget())
        self.statusBar.showMessage(f"File saved in {os.path.dirname(filePath)}", 4000)

    def saveFileAs(self):
        filePath, _ = QFileDialog.getSaveFileName(
            self, "Save File", "", "All Files (*)"
        )
        if filePath:
            currentIndex = self.tabWidget.currentIndex()
            currentWidget = self.tabWidget.currentWidget()
            content = (
                currentWidget.text()
                if isinstance(currentWidget, QsciScintilla)
                else currentWidget.toPlainText()
            )

            worker = FileWorker(filePath, content, mode="w")
            worker.signals.finished.connect(
                lambda fp, _: self.onFileSaveAsFinished(fp, currentIndex)
            )
            worker.signals.error.connect(
                lambda e: self.showErrorMessage("Error saving file", e)
            )
            self.threadPool.start(worker)

    def onFileSaveAsFinished(self, filePath, currentIndex):
        self.filePathDict[currentIndex] = filePath
        fileName = os.path.basename(filePath)
        self.tabWidget.setTabText(currentIndex, fileName)
        self.removeUnsavedChangesMarker(self.tabWidget.currentWidget())
        self.statusBar.showMessage(f"File saved as: {filePath}", 4000)

    def removeUnsavedChangesMarker(self, codespace):
        UNSAVED_CHANGES_MARKER_NUM = 9
        codespace.markerDeleteAll(UNSAVED_CHANGES_MARKER_NUM)

    def isModified(self):
        currentWidget = self.tabWidget.currentWidget()
        return (
            currentWidget.isModified()
            if isinstance(currentWidget, QsciScintilla)
            else currentWidget.document().isModified()
        )

    def openFolder(self):
        folderPath = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folderPath:
            self.fileTree.setRootFolder(folderPath)
            self.folderOpened.emit(folderPath)

    def getTextStats(self, widget):
        if isinstance(widget, QTextEdit):
            cursor = widget.textCursor()
            text = widget.toPlainText()
            return (
                cursor.blockNumber() + 1,
                cursor.columnNumber() + 1,
                widget.document().blockCount(),
                len(text.split()),
            )
        elif isinstance(widget, QsciScintilla):
            lineNumber, columnNumber = widget.getCursorPosition()
            text = widget.text()
            return (
                lineNumber + 1,
                columnNumber + 1,
                widget.lines(),
                len(text.split()),
            )

    def updateStatusBarWithLexer(self):
        currentWidget = self.tabWidget.currentWidget()
        if currentWidget:
            filePath = self.filePathDict.get(self.tabWidget.currentIndex())
            if filePath:
                fileExtension = filePath.split(".")[-1]
                lexer = self.lexerManager.get_lexer(fileExtension)
                lexerName = type(lexer).__name__ if lexer else "None"
            else:
                lexerName = "None"
        else:
            lexerName = "None"
        self.statusBar.updateLexer(lexerName)

    def updateStatusBar(self):
        currentWidget = self.tabWidget.currentWidget()
        if isinstance(currentWidget, (QTextEdit, QsciScintilla)):
            lineNumber, columnNumber, totalLines, words = self.getTextStats(
                currentWidget
            )
            self.statusBar.updateStats(lineNumber, columnNumber, totalLines, words)

            filePath = self.filePathDict.get(self.tabWidget.currentIndex())
            if filePath:
                encoding = self.getFileEncoding(filePath)
                lineEnding = self.getLineEnding(currentWidget)
                fileSize = self.getFileSize(filePath)

                self.statusBar.updateEncoding(encoding)
                self.statusBar.updateLineEnding(lineEnding)
                self.statusBar.updateFileSize(fileSize)
            editMode = "Edit" if not currentWidget.isReadOnly() else "ReadOnly"
            self.statusBar.updateEditMode(editMode)

    def getFileEncoding(self, filePath):
        try:
            with open(filePath, "rb") as file:
                raw = file.read(4096)
            result = chardet.detect(raw)
            return result["encoding"] or "Unknown"
        except Exception:
            return "Unknown"

    def getLineEnding(self, widget):
        if isinstance(widget, QsciScintilla):
            eol_mode = widget.eolMode()
            if eol_mode == QsciScintilla.EolMode.EolWindows:
                return "CRLF"
            elif eol_mode == QsciScintilla.EolMode.EolUnix:
                return "LF"
            elif eol_mode == QsciScintilla.EolMode.EolMac:
                return "CR"
        elif isinstance(widget, QTextEdit):
            text = widget.toPlainText()
            if "\r\n" in text:
                return "CRLF"
            elif "\n" in text:
                return "LF"
            elif "\r" in text:
                return "CR"
        return "Unknown"

    def getFileSize(self, filePath):
        try:
            return os.path.getsize(filePath) / 1024  # Size in KB
        except Exception:
            return 0

    def toggleEditMode(self):
        currentWidget = self.tabWidget.currentWidget()
        if isinstance(currentWidget, QsciScintilla) and hasattr(
            currentWidget, "toggle_edit_mode"
        ):
            currentWidget.toggle_edit_mode(
                prompt=False
            )  # Don't prompt when using shortcut
        self.updateStatusBar()
