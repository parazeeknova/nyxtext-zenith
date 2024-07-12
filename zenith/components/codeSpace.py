import os
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from threading import Thread

from lupa import LuaRuntime  # type: ignore
from PyQt6.Qsci import QsciLexerCPP, QsciLexerJavaScript, QsciLexerPython, QsciScintilla
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QMessageBox

from ..framework.lexer_manager import LexerManager
from ..scripts.roman import toRoman

codespace_counter = 0
lua = LuaRuntime(unpack_returned_tuples=True)

# Create a ThreadPool
thread_pool = ThreadPoolExecutor(max_workers=4)


def load_color_schemes():
    scheme = r"zenith\color_schemes.lua"
    try:
        with open(scheme, "r") as file:
            lua_code = file.read()
        return lua.execute(lua_code)
    except FileNotFoundError:
        QMessageBox.warning(None, "Error", "Color schemes file not found.")
    except Exception as e:
        QMessageBox.warning(None, "Error", f"An unexpected error occurred: {e}")
    return {}


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

    def set_text_thread():
        if isinstance(content, str):
            codespace.setText(content)
        else:
            codespace.setText("")

    thread_pool.submit(set_text_thread)

    with codeSpaceContextManager(codespace) as C:
        # Load color schemes asynchronously
        color_schemes_future = thread_pool.submit(load_color_schemes)

        C.file_path = file_path
        lexer_manager = LexerManager()

        def setup_lexer():
            if C.file_path:
                file_extension = os.path.splitext(C.file_path)[1][1:]
                lexer = lexer_manager.get_lexer(file_extension)
                if lexer:
                    customize_func = None
                    if isinstance(lexer, QsciLexerPython):
                        customize_func = lexer_manager.customize_python_lexer
                    elif isinstance(lexer, QsciLexerJavaScript):
                        customize_func = lexer_manager.customize_javascript_lexer
                    elif isinstance(lexer, QsciLexerCPP):
                        customize_func = lexer_manager.customize_cpp_lexer

                    if customize_func:
                        thread_pool.submit(customize_func, lexer)
                    C.setLexer(lexer)

        color_schemes = color_schemes_future.result()  # Wait for color schemes to load

        C.setBraceMatching(QsciScintilla.BraceMatch.SloppyBraceMatch)
        C.setMatchedBraceBackgroundColor(QColor(color_schemes["matched_brace_bg"]))
        C.setMatchedBraceForegroundColor(QColor("matched_brace_fg"))
        C.setUnmatchedBraceBackgroundColor(QColor(color_schemes["unmatched_brace_bg"]))
        C.setUnmatchedBraceForegroundColor(QColor(color_schemes["unmatched_brace_fg"]))

        setup_lexer()

        romanTitle = f"Codespace {toRoman(codespace_counter)}"
        tabIndex = tabWidget.addTab(C, romanTitle)
        tabWidget.setCurrentIndex(tabIndex)

        C.setUtf8(True)
        C.setCaretForegroundColor(QColor(color_schemes["caret"]))

        # Margin 0: Symbol margin
        C.setMarginType(0, QsciScintilla.MarginType.SymbolMargin)
        C.setMarginWidth(0, 10)
        C.setMarginMarkerMask(1, 0b1111111111111111)

        # Margin 1: Line numbers
        C.setMarginType(1, QsciScintilla.MarginType.NumberMargin)
        C.setMarginWidth(1, 30)
        C.setMarginsForegroundColor(QColor(color_schemes["margin_fg"]))
        C.setMarginsBackgroundColor(QColor(color_schemes["margin_bg"]))

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
        C.setFolding(QsciScintilla.FoldStyle.BoxedTreeFoldStyle, 2)
        C.setFoldMarginColors(
            QColor(color_schemes["folding_bg"]), QColor(color_schemes["folding_fg"])
        )

        # Marker settings for folding
        C.markerDefine(
            QsciScintilla.MarkerSymbol.BoxedPlus, QsciScintilla.SC_MARKNUM_FOLDEROPEN
        )
        C.markerDefine(
            QsciScintilla.MarkerSymbol.BoxedMinus, QsciScintilla.SC_MARKNUM_FOLDER
        )
        C.setMarkerBackgroundColor(
            QColor(color_schemes["marker_text"]), QsciScintilla.SC_MARKNUM_FOLDEROPEN
        )
        C.setMarkerBackgroundColor(
            QColor(color_schemes["marker_text"]), QsciScintilla.SC_MARKNUM_FOLDER
        )
        C.setMarkerForegroundColor(
            QColor(color_schemes["marker"]), QsciScintilla.SC_MARKNUM_FOLDEROPEN
        )
        C.setMarkerForegroundColor(
            QColor(color_schemes["marker"]), QsciScintilla.SC_MARKNUM_FOLDER
        )

        C.setIndentationGuidesBackgroundColor(QColor(color_schemes["intend"]))
        C.setIndentationGuidesForegroundColor(QColor(color_schemes["intend"]))

        BREAKPOINT_MARKER_NUM = 8  # Arbitrary marker number for breakpoints
        C.markerDefine(QsciScintilla.MarkerSymbol.Circle, BREAKPOINT_MARKER_NUM)
        C.setMarkerBackgroundColor(
            QColor(color_schemes["breakpoint"]), BREAKPOINT_MARKER_NUM
        )

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
        C.setMarkerBackgroundColor(
            QColor(color_schemes["unsaved"]), UNSAVED_CHANGES_MARKER_NUM
        )

        def on_text_changed():
            current_line, _ = C.getCursorPosition()
            C.markerAdd(current_line, UNSAVED_CHANGES_MARKER_NUM)
            C.setModified(True)

        C.textChanged.connect(on_text_changed)
        text_change_queue = Queue()

        def text_change_worker():
            while True:
                line = text_change_queue.get()
                if line is None:
                    break
                C.markerAdd(line, UNSAVED_CHANGES_MARKER_NUM)
                C.setModified(True)

        text_change_thread = Thread(target=text_change_worker)
        text_change_thread.start()

        def on_text_changed():
            current_line, _ = C.getCursorPosition()
            text_change_queue.put(current_line)

        C.textChanged.connect(on_text_changed)

        # Clean up the text change thread when the Codespace is closed
        def cleanup():
            text_change_queue.put(None)
            text_change_thread.join()

        C.destroyed.connect(cleanup)

    return C
