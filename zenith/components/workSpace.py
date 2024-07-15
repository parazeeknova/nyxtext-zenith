from PyQt6.QtWidgets import QTextEdit

from ..scripts.roman import toRoman


def Workspace(self, content="", fileName=None):
    self.tabCounter += 1
    newTab = QTextEdit()
    newTab.setStyleSheet("QTextEdit {border: none;}")
    if isinstance(content, str):
        newTab.setText(content)
    else:
        newTab.setText("")

    tabTitle = fileName if fileName else f"Workspace {toRoman(self.tabCounter)}"
    tabIndex = self.tabWidget.addTab(newTab, tabTitle)
    self.tabWidget.setCurrentIndex(tabIndex)

    def update_status_bar():
        parent = self.tabWidget.parent()
        while parent is not None:
            if hasattr(parent, "updateStatusBar"):
                parent.updateStatusBar()
                break
            parent = parent.parent()

    newTab.textChanged.connect(update_status_bar)
    newTab.cursorPositionChanged.connect(update_status_bar)

    # Update status bar immediately after creating the workspace
    update_status_bar()
