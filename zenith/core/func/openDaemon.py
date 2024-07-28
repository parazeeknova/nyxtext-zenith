import logging
import os

import chardet
from PyQt6.Qsci import QsciScintilla
from PyQt6.QtWidgets import QFileDialog, QTextEdit

from ...components.codeSpace import Codespace
from ...components.workSpace import Workspace
from ...core.langFeatures.python_support import PythonFeatures
from ...scripts.color_scheme_loader import color_schemes
from .fileWorker import FileWorker


class OpenDaemon:
    def __init__(self, main_window):
        self.main_window = main_window

    def centralizedOpenFile(self, filePath):
        for tabIndex, openFilePath in self.main_window.filePathDict.items():
            if openFilePath == filePath:
                self.main_window.tabWidget.setCurrentIndex(tabIndex)
                return

        cached_content = self.main_window.fileCache.get(filePath)
        if cached_content is not None:
            self.onFileOpenFinished(filePath, cached_content)
        else:
            worker = FileWorker(filePath)
            worker.signals.finished.connect(self.onFileOpenFinished)
            worker.signals.error.connect(
                lambda e: self.main_window.showErrorMessage("Error opening file", e)
            )
            self.main_window.workers.append(worker)
            self.main_window.threadPool.start(worker)

    def onFileOpenFinished(self, filePath, content):
        try:
            fileName = os.path.basename(filePath)
            folderName = os.path.basename(os.path.dirname(filePath))
            self.main_window.statusBar.showLexerLoadingMessage()
            self.main_window.titleBar.updateTitle(folderName, fileName)

            if filePath.endswith(".txt"):
                tab = Workspace(self.main_window, content, fileName=fileName)
            else:
                tab = Codespace(self.main_window.tabWidget, content, file_path=filePath)

            # Detect and set the correct line ending
            if isinstance(tab, QsciScintilla):
                if "\r\n" in content:
                    tab.setEolMode(QsciScintilla.EolMode.EolWindows)
                elif "\r" in content:
                    tab.setEolMode(QsciScintilla.EolMode.EolMac)
                else:
                    tab.setEolMode(QsciScintilla.EolMode.EolUnix)

            tabIndex = self.main_window.tabWidget.addTab(tab, fileName)
            self.main_window.filePathDict[tabIndex] = filePath
            self.main_window.tabWidget.setCurrentIndex(tabIndex)
            self.main_window.statusBar.showMessage(f"Opened file: {filePath}", 4000)

            self.main_window.updateStatusBar()

            self.main_window.workers = [
                w for w in self.main_window.workers if w.file_path != filePath
            ]
            self.main_window.fileCache.set(filePath, content)

            # Connect the cursorPositionChanged signal for the new tab
            if isinstance(tab, QsciScintilla):
                tab.cursorPositionChanged.connect(self.main_window.updateStatusBar)

        except Exception as e:
            self.main_window.showErrorMessage("Error processing opened file", str(e))

        except Exception as e:
            self.main_window.showErrorMessage("Error processing opened file", str(e))

    def openFile(self):
        filePath, _ = QFileDialog.getOpenFileName(
            self.main_window, "Open File", "", "All Files (*)"
        )
        if filePath:
            self.centralizedOpenFile(filePath)
            self.main_window.terminal.change_directory(os.path.dirname(filePath))

    def openFileFromTree(self, filePath):
        try:
            self.centralizedOpenFile(filePath)
            currentWidget = self.main_window.tabWidget.currentWidget()
            if isinstance(currentWidget, QsciScintilla) and hasattr(
                currentWidget, "toggle_edit_mode"
            ):
                currentWidget.setReadOnly(True)
                currentWidget.markerDeleteAll(11)
                currentWidget.markerAdd(0, 10)

            if filePath.endswith(".py"):
                try:
                    python_features = PythonFeatures(currentWidget, color_schemes)
                    currentWidget.python_features = python_features
                    python_features.updateRequired.connect(currentWidget.recolor)
                    logging.info(f"PythonFeatures initialized for file: {filePath}")
                except Exception as e:
                    logging.exception(f"Error initializing PythonFeatures: {e}")
            self.main_window.updateStatusBarWithLexer()
            self.main_window.updateStatusBar()
        except Exception as e:
            logging.exception(f"Error in openFileFromTree: {e}")

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

    def openFolder(self):
        folderPath = QFileDialog.getExistingDirectory(self.main_window, "Select Folder")
        if folderPath:
            self.main_window.fileTree.setRootFolder(folderPath)
            self.main_window.folderOpened.emit(folderPath)
            self.main_window.terminal.change_directory(folderPath)
