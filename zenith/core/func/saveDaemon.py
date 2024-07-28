import os

from PyQt6.Qsci import QsciScintilla
from PyQt6.QtWidgets import QFileDialog, QTextEdit

from .fileWorker import FileWorker


class SaveDaemon:
    def __init__(self, main_window):
        self.main_window = main_window

    def saveAllTabs(self):
        for i in range(self.main_window.tabWidget.count()):
            if self.isModified(i):
                self.main_window.tabWidget.setCurrentIndex(i)
                self.saveFile()

    def isModified(self, index=None):
        if index is None:
            index = self.main_window.tabWidget.currentIndex()
        widget = self.main_window.tabWidget.widget(index)
        if isinstance(widget, QsciScintilla):
            return widget.isModified()
        elif isinstance(widget, QTextEdit):
            return widget.document().isModified()
        return False

    def saveFile(self):
        currentIndex = self.main_window.tabWidget.currentIndex()
        filePath = self.main_window.filePathDict.get(currentIndex)

        if filePath:
            currentWidget = self.main_window.tabWidget.currentWidget()
            content = (
                currentWidget.text()
                if isinstance(currentWidget, QsciScintilla)
                else currentWidget.toPlainText()
            )

            if isinstance(currentWidget, QsciScintilla):
                eol_mode = currentWidget.eolMode()
                if eol_mode == QsciScintilla.EolMode.EolWindows:
                    content = content.replace("\n", "\r\n")
                elif eol_mode == QsciScintilla.EolMode.EolUnix:
                    content = content.replace("\r\n", "\n")
                elif eol_mode == QsciScintilla.EolMode.EolMac:
                    content = content.replace("\n", "\r")

            worker = FileWorker(filePath, content, mode="w")
            worker.signals.finished.connect(self.onFileSaveFinished)
            worker.signals.error.connect(
                lambda e: self.main_window.showErrorMessage("Error saving file", e)
            )
            self.main_window.workers.append(worker)
            self.main_window.threadPool.start(worker)

            # Update cache with new content
            self.main_window.fileCache.set(filePath, content)
        else:
            self.saveFileAs()

        currentWidget = self.main_window.tabWidget.currentWidget()
        if isinstance(currentWidget, QsciScintilla):
            currentWidget.setModified(False)
        elif isinstance(currentWidget, QTextEdit):
            currentWidget.document().setModified(False)

        print(f"File saved. Is modified: {self.isModified()}")  # Debug print

    def onFileSaveFinished(self, filePath, _):
        currentWidget = self.main_window.tabWidget.currentWidget()
        if isinstance(currentWidget, QsciScintilla):
            currentWidget.setModified(False)
        elif isinstance(currentWidget, QTextEdit):
            currentWidget.document().setModified(False)

        self.removeUnsavedChangesMarker(currentWidget)
        self.main_window.statusBar.showMessage(f"File saved: {filePath}", 4000)
        self.main_window.workers = [
            w for w in self.main_window.workers if w.file_path != filePath
        ]

    def saveFileAs(self):
        currentIndex = self.main_window.tabWidget.currentIndex()
        currentWidget = self.main_window.tabWidget.currentWidget()
        initialPath = self.main_window.filePathDict.get(currentIndex, "")
        filePath, _ = QFileDialog.getSaveFileName(
            self.main_window, "Save File As", initialPath, "All Files (*)"
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
                lambda e: self.main_window.showErrorMessage("Error saving file", e)
            )
            self.main_window.workers.append(worker)
            self.main_window.threadPool.start(worker)

    def onFileSaveAsFinished(self, filePath, currentIndex):
        self.main_window.filePathDict[currentIndex] = filePath
        fileName = os.path.basename(filePath)
        self.main_window.tabWidget.setTabText(currentIndex, fileName)
        currentWidget = self.main_window.tabWidget.widget(currentIndex)
        if isinstance(currentWidget, QsciScintilla):
            currentWidget.setModified(False)
        elif isinstance(currentWidget, QTextEdit):
            currentWidget.document().setModified(False)

        self.removeUnsavedChangesMarker(currentWidget)
        self.main_window.statusBar.showMessage(f"File saved as: {filePath}", 4000)
        self.main_window.workers = [
            w for w in self.main_window.workers if w.file_path != filePath
        ]

    def removeUnsavedChangesMarker(self, codespace):
        UNSAVED_CHANGES_MARKER_NUM = 9
        codespace.markerDeleteAll(UNSAVED_CHANGES_MARKER_NUM)
