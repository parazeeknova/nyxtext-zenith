import os

from PyQt6.Qsci import QsciScintilla
from PyQt6.QtGui import QColor

from ..framework.lexer_manager import LexerManager
from ..scripts.roman import toRoman

codespace_counter = 0


class codeSpaceContextManager:
    def __init__(self, codespace):
        self.codespace = codespace

    def __enter__(self):
        return self.codespace

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass  # Cleanup


def Codespace(tabWidget, content="", file_path=None):
    global codespace_counter
    codespace_counter += 1
    codespace = QsciScintilla()
    if isinstance(content, str):
        codespace.setText(content)
    else:
        codespace.setText("")

    with codeSpaceContextManager(codespace) as C:
        C.file_path = file_path
        lexer_manager = LexerManager()

        def setup_lexer():
            if C.file_path:
                file_extension = os.path.splitext(C.file_path)[1][1:]
                lexer = lexer_manager.get_lexer(file_extension)
                if lexer:
                    C.setLexer(lexer)

        setup_lexer()

        romanTitle = f"Codespace {toRoman(codespace_counter)}"
        tabIndex = tabWidget.addTab(C, romanTitle)
        tabWidget.setCurrentIndex(tabIndex)

        C.setUtf8(True)
        C.setCaretForegroundColor(QColor("#fff"))

        # Margin 0: Symbol margin
        C.setMarginType(0, QsciScintilla.MarginType.SymbolMargin)
        C.setMarginWidth(0, 10)
        C.setMarginMarkerMask(1, 0b1111111111111111)

        # Margin 1: Line numbers
        C.setMarginType(1, QsciScintilla.MarginType.NumberMargin)
        C.setMarginWidth(1, 30)
        C.setMarginsForegroundColor(QColor("#fff"))
        C.setMarginsBackgroundColor(QColor("#444"))

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
        C.setFoldMarginColors(QColor("#444"), QColor("#444"))

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

        BREAKPOINT_MARKER_NUM = 8  # Arbitrary marker number for breakpoints
        C.markerDefine(QsciScintilla.MarkerSymbol.Circle, BREAKPOINT_MARKER_NUM)
        C.setMarkerBackgroundColor(QColor("#ed8796"), BREAKPOINT_MARKER_NUM)

        def on_margin_clicked(nmargin, nline):
            if nmargin == 1:
                if C.markersAtLine(nline) & (1 << BREAKPOINT_MARKER_NUM):
                    C.markerDelete(nline, BREAKPOINT_MARKER_NUM)
                else:
                    C.markerAdd(nline, BREAKPOINT_MARKER_NUM)

        C.marginClicked.connect(on_margin_clicked)
        C.setMarginSensitivity(1, True)

        UNSAVED_CHANGES_MARKER_NUM = 9  # Arbitrary marker number for unsaved changes
        C.markerDefine(
            QsciScintilla.MarkerSymbol.LeftRectangle, UNSAVED_CHANGES_MARKER_NUM
        )
        C.setMarkerBackgroundColor(QColor("#a6da95"), UNSAVED_CHANGES_MARKER_NUM)

        def on_text_changed():
            current_line, _ = C.getCursorPosition()
            C.markerAdd(current_line, UNSAVED_CHANGES_MARKER_NUM)
            C.setModified(True)

        C.textChanged.connect(on_text_changed)

    return C
