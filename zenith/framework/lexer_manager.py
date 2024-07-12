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
from PyQt6.QtWidgets import QMessageBox

from ..lexers.cpp_lexer import customize_cpp_lexer
from ..lexers.javascript_lexer import customize_javascript_lexer
from ..lexers.python_lexer import customize_python_lexer

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
        self.color_schemes = self.load_color_schemes()

        self.customize_python_lexer = lambda lexer: customize_python_lexer(
            lexer, self.color_schemes
        )
        self.customize_javascript_lexer = lambda lexer: customize_javascript_lexer(
            lexer, self.color_schemes
        )
        self.customize_cpp_lexer = lambda lexer: customize_cpp_lexer(
            lexer, self.color_schemes
        )

    def load_color_schemes(self):
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

    def get_lexer(self, file_extension):
        return self.lexers.get(file_extension.lower(), None)

    def get_lexer_names(self):
        return list(self.lexers.keys())

    def get_lexer_by_name(self, lexer_name):
        for ext, lexer in self.lexers.items():
            if lexer.__class__.__name__ == lexer_name:
                return lexer
        return None
