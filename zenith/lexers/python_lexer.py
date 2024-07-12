# python_lexer.py
from PyQt6.Qsci import QsciLexerPython
from PyQt6.QtGui import QColor, QFont


def customize_python_lexer(lexer, color_schemes):
    default_font = QFont("JetBrainsMono Nerd Font", 10)
    lexer.setFont(default_font)

    comment_font = QFont("JetBrainsMono Nerd Font", 10, italic=True)
    lexer.setFont(comment_font, QsciLexerPython.Comment)

    keyword_font = QFont("JetBrainsMono Nerd Font", 10, weight=QFont.Weight.Bold)
    lexer.setFont(keyword_font, QsciLexerPython.Keyword)

    number_font = QFont("JetBrainsMono Nerd Font", 10, weight=QFont.Weight.Bold)
    lexer.setFont(number_font, QsciLexerPython.Number)

    for style, color_key in [
        (QsciLexerPython.Default, "default"),
        (QsciLexerPython.Keyword, "keyword"),
        (QsciLexerPython.Comment, "comment"),
        (QsciLexerPython.DoubleQuotedString, "string"),
        (QsciLexerPython.SingleQuotedString, "string2"),
        (QsciLexerPython.Number, "numbers"),
        (QsciLexerPython.ClassName, "class"),
        (QsciLexerPython.FunctionMethodName, "func"),
        (QsciLexerPython.Operator, "operators"),
    ]:
        lexer.setColor(QColor(color_schemes[color_key]), style)
