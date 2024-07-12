from lupa import LuaRuntime  # type: ignore
from PyQt6.Qsci import (
    QsciLexerAVS,
    QsciLexerBash,
    QsciLexerBatch,
    QsciLexerCMake,
    QsciLexerCoffeeScript,
    QsciLexerCPP,
    QsciLexerCSharp,
    QsciLexerCSS,
    QsciLexerD,
    QsciLexerDiff,
    QsciLexerFortran,
    QsciLexerFortran77,
    QsciLexerHTML,
    QsciLexerIDL,
    QsciLexerJava,
    QsciLexerJavaScript,
    QsciLexerJSON,
    QsciLexerLua,
    QsciLexerMakefile,
    QsciLexerMarkdown,
    QsciLexerMatlab,
    QsciLexerOctave,
    QsciLexerPascal,
    QsciLexerPerl,
    QsciLexerPO,
    QsciLexerPostScript,
    QsciLexerPOV,
    QsciLexerProperties,
    QsciLexerPython,
    QsciLexerRuby,
    QsciLexerSpice,
    QsciLexerSQL,
    QsciLexerTCL,
    QsciLexerTeX,
    QsciLexerVerilog,
    QsciLexerVHDL,
    QsciLexerXML,
    QsciLexerYAML,
)
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtWidgets import QMessageBox

lua = LuaRuntime(unpack_returned_tuples=True)


class LexerManager:
    def __init__(self):
        self.lexers = {
            # A
            "avs": QsciLexerAVS(),
            # B
            "sh": QsciLexerBash(),
            "bash": QsciLexerBash(),
            "bat": QsciLexerBatch(),
            "cmd": QsciLexerBatch(),
            # C
            "cmake": QsciLexerCMake(),
            "coffee": QsciLexerCoffeeScript(),
            "c": QsciLexerCPP(),
            "cpp": QsciLexerCPP(),
            "h": QsciLexerCPP(),
            "hpp": QsciLexerCPP(),
            "cxx": QsciLexerCPP(),
            "cs": QsciLexerCSharp(),
            "css": QsciLexerCSS(),
            # D
            "d": QsciLexerD(),
            "diff": QsciLexerDiff(),
            "patch": QsciLexerDiff(),
            # F
            "f": QsciLexerFortran(),
            "for": QsciLexerFortran(),
            "f77": QsciLexerFortran77(),
            # H
            "html": QsciLexerHTML(),
            "htm": QsciLexerHTML(),
            # I
            "idl": QsciLexerIDL(),
            # J
            "java": QsciLexerJava(),
            "js": QsciLexerJavaScript(),
            "json": QsciLexerJSON(),
            # L
            "lua": QsciLexerLua(),
            # M
            "makefile": QsciLexerMakefile(),
            "mk": QsciLexerMakefile(),
            "md": QsciLexerMarkdown(),
            "markdown": QsciLexerMarkdown(),
            "m": QsciLexerMatlab(),
            # O
            "octave": QsciLexerOctave(),
            # P
            "pas": QsciLexerPascal(),
            "pl": QsciLexerPerl(),
            "pm": QsciLexerPerl(),
            "po": QsciLexerPO(),
            "ps": QsciLexerPostScript(),
            "pov": QsciLexerPOV(),
            "ini": QsciLexerProperties(),
            "conf": QsciLexerProperties(),
            "py": QsciLexerPython(),
            "pyw": QsciLexerPython(),
            # R
            "rb": QsciLexerRuby(),
            "ruby": QsciLexerRuby(),
            # S
            "spice": QsciLexerSpice(),
            "sql": QsciLexerSQL(),
            # T
            "tcl": QsciLexerTCL(),
            "tex": QsciLexerTeX(),
            # V
            "v": QsciLexerVerilog(),
            "vhdl": QsciLexerVHDL(),
            "vhd": QsciLexerVHDL(),
            # X
            "xml": QsciLexerXML(),
            # Y
            "yml": QsciLexerYAML(),
            "yaml": QsciLexerYAML(),
        }

    scheme = r"zenith\color_schemes.lua"
    try:
        with open(scheme, "r") as file:
            lua_code = file.read()
        global color_schemes
        color_schemes = lua.execute(lua_code)
    except FileNotFoundError:
        QMessageBox.warning(None, "Error", "Color schemes file not found.")
    except Exception as e:
        QMessageBox.warning(None, "Error", f"An unexpected error occurred: {e}")

    def get_lexer(self, file_extension):
        return self.lexers.get(file_extension.lower(), None)

    def get_lexer_names(self):
        return list(self.lexers.keys())

    def get_lexer_by_name(self, lexer_name):
        for ext, lexer in self.lexers.items():
            if lexer.__class__.__name__ == lexer_name:
                return lexer
        return None

    def customize_python_lexer(lexer):
        default_font = QFont("JetBrainsMono Nerd Font", 10)
        lexer.setFont(default_font)

        comment_font = QFont("JetBrainsMono Nerd Font", 10)
        comment_font.setItalic(True)
        lexer.setFont(comment_font, QsciLexerPython.Comment)

        keyword_font = QFont("JetBrainsMono Nerd Font", 10)
        keyword_font.setBold(True)
        lexer.setFont(keyword_font, QsciLexerPython.Keyword)

        number_font = QFont("JetBrainsMono Nerd Font", 10)
        number_font.setBold(True)
        lexer.setFont(number_font, QsciLexerPython.Number)

        lexer.setColor(QColor(color_schemes["default"]), QsciLexerPython.Default)
        lexer.setColor(QColor(color_schemes["keyword"]), QsciLexerPython.Keyword)
        lexer.setColor(QColor(color_schemes["comment"]), QsciLexerPython.Comment)
        lexer.setColor(
            QColor(color_schemes["string"]), QsciLexerPython.DoubleQuotedString
        )
        lexer.setColor(
            QColor(color_schemes["string2"]), QsciLexerPython.SingleQuotedString
        )
        lexer.setColor(QColor(color_schemes["numbers"]), QsciLexerPython.Number)
        lexer.setColor(QColor(color_schemes["class"]), QsciLexerPython.ClassName)
        lexer.setColor(
            QColor(color_schemes["func"]), QsciLexerPython.FunctionMethodName
        )
        lexer.setColor(QColor(color_schemes["operators"]), QsciLexerPython.Operator)
        lexer.setColor(QColor(color_schemes["brace"]), QsciLexerPython.Operator)
