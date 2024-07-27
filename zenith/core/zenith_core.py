import logging
import os

from lupa import LuaRuntime  # type: ignore
from PyQt6.Qsci import QsciScintilla
from PyQt6.QtCore import (
    QEasingCurve,
    QPropertyAnimation,
    QSize,
    Qt,
    QThreadPool,
    pyqtSignal,
)
from PyQt6.QtGui import QColor, QIcon, QPalette
from PyQt6.QtWidgets import (
    QApplication,
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
from .func.openDaemon import OpenDaemon
from .func.saveDaemon import SaveDaemon

logging.basicConfig(
    level=logging.DEBUG,
    filename="zenith_debug.log",
    filemode="w",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

powershellIcon = resource(r"../media/filetree/powershell.svg")


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

        self.openDaemon = OpenDaemon(self)
        self.saveDaemon = SaveDaemon(self)
        self.setupUI()
        self.setupConnections()
        self.setupTerminal()

        self.maximizeAnimation = QPropertyAnimation(self, b"geometry")
        self.maximizeAnimation.setDuration(300)
        self.maximizeAnimation.setEasingCurve(QEasingCurve.Type.InOutQuad)

    def animatedMaximize(self):
        if not self.isMaximized():
            self.maximizeAnimation.setStartValue(self.geometry())
            self.maximizeAnimation.setEndValue(self.screen().availableGeometry())
            self.maximizeAnimation.start()
        else:
            self.showNormal()

    def animatedMinimize(self):
        self.maximizeAnimation.setStartValue(self.geometry())
        end_rect = self.geometry()
        end_rect.setHeight(0)
        self.maximizeAnimation.setEndValue(end_rect)
        self.maximizeAnimation.finished.connect(self.hide)
        self.maximizeAnimation.start()

    # Override these methods
    def showMaximized(self):
        self.animatedMaximize()

    def showMinimized(self):
        self.animatedMinimize()

    def setupUI(self):
        self.setWindowTitle("Zenith")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon(resource(r"../media/icon.ico")))

        self.setApplicationPalette()

        self.titleBar = CustomTitleBar(self, self)
        if self.preferences.get("hide_default_titlebar", False):
            self.setMenuWidget(self.titleBar)
        else:
            self.setMenuBar(self.titleBar.menuBar(self))

        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        layout = QVBoxLayout(centralWidget)

        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        layout.addWidget(self.splitter)

        self.tabWidget = tabRow(self, self.splitter)

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

        self.setStyleSheet(
            """
            QMainWindow {
                border-radius: 10px;
                background-color: #24273a;
            }
        """
        )

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

    def openFile(self):
        self.openDaemon.openFile()

    def setupConnections(self):
        logging.info("Setting up connections")
        self.fileTree.visibilityChanged.connect(self.adjustSplitter)
        self.fileTree.dockingChanged.connect(self.handleDockingChange)
        self.tabWidget.currentChanged.connect(self.onTabChange)
        self.fileTree.fileTree.fileSelected.connect(self.openDaemon.openFileFromTree)
        self.tabWidget.tabCloseRequested.connect(self.handleTabClose)
        self.terminalButton.clicked.connect(self.toggleTerminal)
        logging.info("Connections set up successfully")

    def closeApplication(self):
        self.closeAllTabs()
        self.fileCache.clear()
        QApplication.quit()

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

    def showErrorMessage(self, title, message):
        QMessageBox.critical(self, title, message)

    def onTabChange(self, index):
        logging.info(f"Tab changed to index {index}")
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

    def openFolder(self):
        self.openDaemon.openFolder()

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
                encoding = self.openDaemon.getFileEncoding(filePath)
                lineEnding = self.openDaemon.getLineEnding(currentWidget)
                fileSize = self.openDaemon.getFileSize(filePath)

                self.statusBar.updateEncoding(encoding)
                self.statusBar.updateLineEnding(lineEnding)
                self.statusBar.updateFileSize(fileSize)
            editMode = "Edit" if not currentWidget.isReadOnly() else "ReadOnly"
            self.statusBar.updateEditMode(editMode)

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

    def show_autocompletion(self):
        current_widget = self.tabWidget.currentWidget()
        if isinstance(current_widget, QsciScintilla) and hasattr(
            current_widget, "python_features"
        ):
            current_widget.autoCompleteFromAll()
            logging.debug("Manual autocompletion triggered")

    def show_calltip(self):
        current_widget = self.tabWidget.currentWidget()
        if isinstance(current_widget, QsciScintilla) and hasattr(
            current_widget, "python_features"
        ):
            current_widget.python_features.show_calltip()
            logging.debug("Manual calltip triggered")

    def handleCursorPositionChanged(self):
        currentWidget = self.tabWidget.currentWidget()
        if isinstance(currentWidget, QsciScintilla):
            currentWidget.cursorPositionChanged.connect(self.updateStatusBar)

    def hasUnsavedChanges(self):
        return any(self.saveDaemon.isModified(i) for i in range(self.tabWidget.count()))

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
                self.saveDaemon.saveAllTabs()
                return True
            elif result == QMessageBox.StandardButton.Discard:
                return True
            else:  # Cancel
                return False
        return True

    def closeTab(self, index):
        if self.saveDaemon.isModified(index):
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
                self.saveDaemon.saveFile()
            elif result == QMessageBox.StandardButton.Cancel:
                return

        if self.tabWidget.count() > 1:
            self.tabWidget.removeTab(index)
            if index in self.filePathDict:
                del self.filePathDict[index]
            self.updateFilePathDict()

        if self.tabWidget.count() == 0:
            self.titleBar.updateTitle(None)
