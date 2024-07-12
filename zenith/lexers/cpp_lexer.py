from PyQt6.Qsci import QsciLexerCPP
from PyQt6.QtGui import QColor, QFont


def customize_cpp_lexer(lexer, color_schemes):
    default_font = QFont("JetBrainsMono Nerd Font", 10)
    lexer.setFont(default_font)

    comment_font = QFont("JetBrainsMono Nerd Font", 10, italic=True)
    lexer.setFont(comment_font, QsciLexerCPP.Comment)

    keyword_font = QFont("JetBrainsMono Nerd Font", 10, weight=QFont.Weight.Bold)
    lexer.setFont(keyword_font, QsciLexerCPP.Keyword)

    for style, color_key in [
        (QsciLexerCPP.Default, "default"),
        (QsciLexerCPP.Keyword, "keyword"),
        (QsciLexerCPP.Comment, "comment"),
        (QsciLexerCPP.DoubleQuotedString, "string"),
        (QsciLexerCPP.SingleQuotedString, "string2"),
        (QsciLexerCPP.Number, "numbers"),
        (QsciLexerCPP.Identifier, "default"),
        (QsciLexerCPP.Operator, "operators"),
        (QsciLexerCPP.PreProcessor, "keyword"),
        (QsciLexerCPP.InactiveDefault, "default"),
        (QsciLexerCPP.InactiveComment, "comment"),
        (QsciLexerCPP.InactiveKeyword, "keyword"),
    ]:
        lexer.setColor(QColor(color_schemes[color_key]), style)
