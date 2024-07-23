import os

import chardet
from lupa import LuaRuntime  # type: ignore
from PyQt6.Qsci import QsciScintilla
from PyQt6.QtCore import (
    Q_ARG,
    QMetaObject,
    QObject,
    QRunnable,
    QSize,
    Qt,
    QThreadPool,
    pyqtSignal,
)
from PyQt6.QtGui import QColor, QIcon, QPalette
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSplitter,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from ..components.codeSpace import Codespace
from ..components.rightSideBar import FileTreeWidget
from ..components.tabTopbar import tabRow
from ..components.terminal import TerminalEmulator
from ..components.workSpace import Workspace
from ..framework.lexer_manager import LexerManager
from ..framework.statusBar import ZenithStatusBar
from ..framework.titleBar import CustomTitleBar
from ..scripts.color_scheme_loader import color_schemes
from ..scripts.def_path import resource
from ..scripts.file_cache import FileCache
from ..scripts.shortcuts import key_shortcuts

powershellIcon = resource(r"../media/filetree/powershell.svg")


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
                QMetaObject.invokeMethod(
                    self.signals,
                    "finished",
                    Qt.ConnectionType.QueuedConnection,
                    Q_ARG(str, self.file_path),
                    Q_ARG(str, content),
                )
            elif self.mode == "w":
                with open(self.file_path, "w", encoding="utf-8") as file:
                    file.write(self.content)
                QMetaObject.invokeMethod(
                    self.signals,
                    "finished",
                    Qt.ConnectionType.QueuedConnection,
                    Q_ARG(str, self.file_path),
                    Q_ARG(str, ""),
                )
        except Exception as e:
            QMetaObject.invokeMethod(
                self.signals,
                "error",
                Qt.ConnectionType.QueuedConnection,
                Q_ARG(str, str(e)),
            )


class Zenith(QMainWindow):
    folderOpened = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.lua = LuaRuntime(unpack_returned_tuples=True)
        self.preferences = self.load_preferences()

        if self.preferences.get("hide_default_titlebar", False):
            self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

        self.threadPool = QThreadPool()
        self.workers = []
        self.lexerManager = LexerManager()
        self.filePathDict = {}
        self.fileCache = FileCache()
        self.tabCounter = 0

        self.setupUI()
        self.setupConnections()
        self.setupTerminal()

    def setupUI(self):
        self.setWindowTitle("Zenith")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon(resource(r"../media/icon.ico")))

        self.setApplicationPalette()

        self.titleBar = CustomTitleBar(self, self)
        if self.preferences.get("hide_default_titlebar", False):
            self.setMenuWidget(self.titleBar)
        else:
            self.setMenuBar(self.titleBar.menuBar)

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

        self.verticalSplitter = QSplitter(Qt.Orientation.Vertical)
        self.verticalSplitter.addWidget(self.splitter)

        self.terminal = TerminalEmulator()
        self.terminal.hide()
        self.verticalSplitter.addWidget(self.terminal)

        self.terminal.setStyleSheet(
            """
            QPlainTextEdit {
                background-color: #1E1E1E;
                color: white;
                font-family: Consolas, Courier, monospace;
            }
            """
        )

        layout.addWidget(self.verticalSplitter)

        self.terminalButton = QPushButton(self)
        self.terminalButton.setIcon(QIcon(powershellIcon))
        self.terminalButton.setIconSize(QSize(16, 16))
        self.terminalButton.setStyleSheet(
            f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                padding: 5px;
            }}
            QPushButton:hover {{
                background-color: {color_schemes['selection_bg']};
            }}
            """
        )
        self.tabWidget.setCornerWidget(self.terminalButton, Qt.Corner.TopRightCorner)

    def setApplicationPalette(self):
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color_schemes["background"]))
        palette.setColor(
            QPalette.ColorRole.WindowText, QColor(color_schemes["foreground"])
        )
        palette.setColor(
            QPalette.ColorRole.Base, QColor(color_schemes["background_codespace"])
        )
        palette.setColor(
            QPalette.ColorRole.AlternateBase, QColor(color_schemes["surface0"])
        )
        palette.setColor(
            QPalette.ColorRole.ToolTipBase, QColor(color_schemes["background"])
        )
        palette.setColor(
            QPalette.ColorRole.ToolTipText, QColor(color_schemes["foreground"])
        )
        palette.setColor(QPalette.ColorRole.Text, QColor(color_schemes["foreground"]))
        palette.setColor(QPalette.ColorRole.Button, QColor(color_schemes["surface1"]))
        palette.setColor(
            QPalette.ColorRole.ButtonText, QColor(color_schemes["foreground"])
        )
        palette.setColor(QPalette.ColorRole.BrightText, QColor(color_schemes["red"]))
        palette.setColor(QPalette.ColorRole.Link, QColor(color_schemes["blue"]))
        palette.setColor(
            QPalette.ColorRole.Highlight, QColor(color_schemes["selection_bg"])
        )
        palette.setColor(
            QPalette.ColorRole.HighlightedText,
            QColor(color_schemes["selection_fg"]),
        )

        self.setPalette(palette)
        QApplication.setPalette(palette)

    def setupConnections(self):
        self.fileTree.visibilityChanged.connect(self.adjustSplitter)
        self.fileTree.dockingChanged.connect(self.handleDockingChange)
        self.tabWidget.currentChanged.connect(self.onTabChange)
        self.fileTree.fileTree.fileSelected.connect(self.openFileFromTree)
        self.tabWidget.tabCloseRequested.connect(self.handleTabClose)
        self.codespace.cursorPositionChanged.connect(self.handleCursorPositionChanged)
        self.terminalButton.clicked.connect(self.toggleTerminal)

    def closeApplication(self):
        self.closeAllTabs()
        self.fileCache.clear()
        QApplication.quit()

    def confirmClose(self, close_all=False):
        if self.hasUnsavedChanges():
            dialog = QMessageBox(self)
            dialog.setWindowTitle("Unsaved Changes")
            dialog.setText("There are unsaved changes. What would you like to do?")
            dialog.setStandardButtons(
                QMessageBox.StandardButton.SaveAll
                | QMessageBox.StandardButton.Discard
                | QMessageBox.StandardButton.Cancel
            )
            dialog.setDefaultButton(QMessageBox.StandardButton.SaveAll)

            result = dialog.exec()
            if result == QMessageBox.StandardButton.SaveAll:
                self.saveAllTabs()
                return True
            elif result == QMessageBox.StandardButton.Discard:
                return True
            else:  # Cancel
                return False
        return True

    def saveAllTabs(self):
        for i in range(self.tabWidget.count()):
            if self.isModified(i):
                self.tabWidget.setCurrentIndex(i)
                self.saveFile()

    def isModified(self, index=None):
        if index is None:
            index = self.tabWidget.currentIndex()
        widget = self.tabWidget.widget(index)
        if isinstance(widget, QsciScintilla):
            return widget.isModified()
        elif isinstance(widget, QTextEdit):
            return widget.document().isModified()
        return False

    def handleCursorPositionChanged(self):
        self.updateStatusBar()

    def hasUnsavedChanges(self):
        return any(self.isModified(i) for i in range(self.tabWidget.count()))

    def addNewTab(self):
        Workspace(self)

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
            self.workers.append(worker)
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
            self.workers = [w for w in self.workers if w.file_path != filePath]
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
            self.terminal.change_directory(os.path.dirname(filePath))

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

    def saveFile(self):
        currentIndex = self.tabWidget.currentIndex()
        filePath = self.filePathDict.get(currentIndex)

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
            self.workers.append(worker)
            self.threadPool.start(worker)

            # Update cache with new content
            self.fileCache.set(filePath, content)
        else:
            self.saveFileAs()

    def onFileSaveFinished(self, filePath, _):
        currentWidget = self.tabWidget.currentWidget()
        if isinstance(currentWidget, QsciScintilla):
            currentWidget.setModified(False)
        elif isinstance(currentWidget, QTextEdit):
            currentWidget.document().setModified(False)

        self.removeUnsavedChangesMarker(currentWidget)
        self.statusBar.showMessage(f"File saved: {filePath}", 4000)
        self.workers = [w for w in self.workers if w.file_path != filePath]

    def saveFileAs(self):
        currentIndex = self.tabWidget.currentIndex()
        currentWidget = self.tabWidget.currentWidget()
        initialPath = self.filePathDict.get(currentIndex, "")
        filePath, _ = QFileDialog.getSaveFileName(
            self, "Save File As", initialPath, "All Files (*)"
        )

        if filePath:
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
            self.workers.append(worker)
            self.threadPool.start(worker)

    def onFileSaveAsFinished(self, filePath, currentIndex):
        self.filePathDict[currentIndex] = filePath
        fileName = os.path.basename(filePath)
        self.tabWidget.setTabText(currentIndex, fileName)
        currentWidget = self.tabWidget.widget(currentIndex)
        if isinstance(currentWidget, QsciScintilla):
            currentWidget.setModified(False)
        elif isinstance(currentWidget, QTextEdit):
            currentWidget.document().setModified(False)

        self.removeUnsavedChangesMarker(currentWidget)
        self.statusBar.showMessage(f"File saved as: {filePath}", 4000)
        self.workers = [w for w in self.workers if w.file_path != filePath]

    def removeUnsavedChangesMarker(self, codespace):
        UNSAVED_CHANGES_MARKER_NUM = 9
        codespace.markerDeleteAll(UNSAVED_CHANGES_MARKER_NUM)

    def openFolder(self):
        folderPath = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folderPath:
            self.fileTree.setRootFolder(folderPath)
            self.folderOpened.emit(folderPath)
            self.terminal.change_directory(folderPath)

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

    def load_preferences(self):
        try:
            with open("zenith/config.lua", "r") as file:
                lua_code = file.read()
            preferences = self.lua.execute(lua_code)
            if preferences is None:
                raise ValueError("Lua script did not return a table")
            return dict(preferences)
        except FileNotFoundError:
            QMessageBox.warning(self, "Error", "Preferences file not found.")
        except ValueError as e:
            QMessageBox.warning(self, "Error", f"Invalid preferences file: {e}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"An unexpected error occurred: {e}")
        return {}

    def closeTab(self, index):
        if self.isModified(index):
            self.tabWidget.setCurrentIndex(index)
            dialog = QMessageBox(self)
            dialog.setWindowTitle("Unsaved Changes")
            dialog.setText(
                f"The file in tab {index + 1} has unsaved changes. "
                "Do you want to save before closing?"
            )
            dialog.setStandardButtons(
                QMessageBox.StandardButton.Save
                | QMessageBox.StandardButton.Discard
                | QMessageBox.StandardButton.Cancel
            )
            dialog.setDefaultButton(QMessageBox.StandardButton.Save)

            result = dialog.exec()
            if result == QMessageBox.StandardButton.Save:
                self.saveFile()
            elif result == QMessageBox.StandardButton.Cancel:
                return

        if self.tabWidget.count() > 1:
            self.tabWidget.removeTab(index)
            if index in self.filePathDict:
                del self.filePathDict[index]
            self.updateFilePathDict()

        if self.tabWidget.count() == 0:
            self.titleBar.updateTitle(None)

    # Update the handleTabClose method
    def handleTabClose(self, index):
        self.closeTab(index)

    def closeEvent(self, event):
        if self.confirmClose(close_all=True):
            self.closeApplication()
            event.accept()
        else:
            event.ignore()

    def setupTerminal(self):
        self.terminal = TerminalEmulator()
        self.terminal.setMinimumHeight(100)
        self.verticalSplitter.addWidget(self.terminal)
        self.terminal.hide()

    def toggleTerminal(self):
        if self.terminal.isVisible():
            self.terminal.hide()
        else:
            self.terminal.show()

    def runCurrentFile(self):
        currentIndex = self.tabWidget.currentIndex()
        filePath = self.filePathDict.get(currentIndex)
        if filePath:
            self.terminal.show()
            self.terminal.run_file(filePath)
