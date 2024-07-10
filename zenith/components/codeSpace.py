from PyQt6.Qsci import QsciScintilla

from ..scripts.roman import toRoman

codespace_counter = 0


def Codespace(tabWidget):
    global codespace_counter
    codespace_counter += 1
    codespace = QsciScintilla()
    codespace.setUtf8(True)
    romanTitle = f"Codespace {toRoman(codespace_counter)}"
    tabIndex = tabWidget.addTab(codespace, romanTitle)
    tabWidget.setCurrentIndex(tabIndex)
