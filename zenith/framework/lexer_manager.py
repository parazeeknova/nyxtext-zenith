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

catppuccin_colors = {
    "default": "#D9E0EE",
    "keyword": "#7dc4e4",
    "operator": "#F8BD96",
    "brace": "#F5C2E7",
    "defclass": "#F8BD96",
    "string": "#ABE9B3",
    "string2": "#F5E0DC",
    "comment": "#89B4FA",
    "self": "#F5E0DC",
    "numbers": "#F5C2E7",
    "class": "#c6a0f6",
    "function": "#F28FAD",
    "operators": "#8aadf4",
}


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

        lexer.setColor(QColor(catppuccin_colors["default"]), QsciLexerPython.Default)
        lexer.setColor(QColor(catppuccin_colors["keyword"]), QsciLexerPython.Keyword)
        lexer.setColor(QColor(catppuccin_colors["comment"]), QsciLexerPython.Comment)
        lexer.setColor(
            QColor(catppuccin_colors["string"]), QsciLexerPython.DoubleQuotedString
        )
        lexer.setColor(
            QColor(catppuccin_colors["string2"]), QsciLexerPython.SingleQuotedString
        )
        lexer.setColor(QColor(catppuccin_colors["numbers"]), QsciLexerPython.Number)
        lexer.setColor(QColor(catppuccin_colors["class"]), QsciLexerPython.ClassName)
        lexer.setColor(
            QColor(catppuccin_colors["function"]), QsciLexerPython.FunctionMethodName
        )
        lexer.setColor(QColor(catppuccin_colors["operators"]), QsciLexerPython.Operator)
