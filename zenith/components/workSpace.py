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
