from PyQt6.QtWidgets import QTextEdit

from ..scripts.roman import toRoman


def Workspace(self, content=""):
    self.tabCounter += 1
    newTab = QTextEdit()
    newTab.setStyleSheet("QTextEdit {border: none;}")
    if isinstance(content, str):
        newTab.setText(content)
    else:
        newTab.setText("")
    romanNumeral = toRoman(self.tabCounter)
    tabIndex = self.tabWidget.addTab(newTab, f"Workspace {romanNumeral}")
    self.tabWidget.setCurrentIndex(tabIndex)
