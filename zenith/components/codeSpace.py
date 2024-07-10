import os

from PyQt6.Qsci import QsciLexerPython, QsciScintilla
from PyQt6.QtGui import QColor

from ..scripts.roman import toRoman

codespace_counter = 0


class codeSpaceContextManager:
    def __init__(self, codespace):
        self.codespace = codespace

    def __enter__(self):
        lexer = QsciLexerPython()
        self.codespace.setLexer(lexer)
        return self.codespace

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass  # Cleanup


def Codespace(tabWidget):
    global codespace_counter
    codespace_counter += 1
    codespace = QsciScintilla()

    with codeSpaceContextManager(codespace) as C:
        romanTitle = f"Codespace {toRoman(codespace_counter)}"
        tabIndex = tabWidget.addTab(C, romanTitle)
        tabWidget.setCurrentIndex(tabIndex)

        C.setUtf8(True)
        C.setCaretForegroundColor(QColor("#fff"))

        # Set up margins
        # Margin 0: Line numbers
        C.setMarginType(0, QsciScintilla.MarginType.NumberMargin)
        C.setMarginWidth(0, 40)
        C.setMarginsForegroundColor(QColor("#fff"))
        C.setMarginsBackgroundColor(QColor("#444"))

        # Margin 1: Symbol margin
        C.setMarginType(1, QsciScintilla.MarginType.SymbolMargin)
        C.setMarginWidth(1, 20)
        C.setMarginMarkerMask(1, 0b1111111111111111)

        # Margin 2: Folding margin
        C.setMarginType(2, QsciScintilla.MarginType.SymbolMargin)
        C.setMarginWidth(2, 15)
        C.setMarginSensitivity(2, True)

        C.setWrapMode(QsciScintilla.WrapMode.WrapWhitespace)
        C.setWrapVisualFlags(QsciScintilla.WrapVisualFlag.WrapFlagInMargin)
        C.setWrapIndentMode(QsciScintilla.WrapIndentMode.WrapIndentIndented)

        if os.name == "nt":
            C.setEolMode(QsciScintilla.EolMode.EolWindows)
        elif os.name == "posix":
            C.setEolMode(QsciScintilla.EolMode.EolUnix)

        C.setIndentationsUseTabs(True)
        C.setTabWidth(4)
        C.setIndentationGuides(True)
        C.setAutoIndent(True)

        # Folding settings
        C.setFolding(QsciScintilla.FoldStyle.PlainFoldStyle, 2)
        C.setFoldMarginColors(QColor("#2E2E2E"), QColor("#2E2E2E"))

        # Marker settings for folding
        C.markerDefine(
            QsciScintilla.MarkerSymbol.BoxedPlus, QsciScintilla.SC_MARKNUM_FOLDEROPEN
        )
        C.markerDefine(
            QsciScintilla.MarkerSymbol.BoxedMinus, QsciScintilla.SC_MARKNUM_FOLDER
        )
        C.setMarkerBackgroundColor(
            QColor("#4E4E4E"), QsciScintilla.SC_MARKNUM_FOLDEROPEN
        )
        C.setMarkerBackgroundColor(QColor("#4E4E4E"), QsciScintilla.SC_MARKNUM_FOLDER)
        C.setMarkerForegroundColor(QColor("white"), QsciScintilla.SC_MARKNUM_FOLDEROPEN)
        C.setMarkerForegroundColor(QColor("white"), QsciScintilla.SC_MARKNUM_FOLDER)

        C.setIndentationGuidesBackgroundColor(QColor("#aaa"))
        C.setIndentationGuidesForegroundColor(QColor("#aaa"))

    return C
