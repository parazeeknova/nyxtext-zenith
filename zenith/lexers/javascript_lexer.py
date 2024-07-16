from PyQt6.Qsci import QsciLexerJavaScript
from PyQt6.QtGui import QColor, QFont


def customize_javascript_lexer(lexer, color_schemes):
    default_font = QFont("JetBrainsMono Nerd Font", 10)
    lexer.setFont(default_font)

    comment_font = QFont("JetBrainsMono Nerd Font", 10, italic=True)
    lexer.setFont(comment_font, QsciLexerJavaScript.Comment)

    keyword_font = QFont("JetBrainsMono Nerd Font", 10, weight=QFont.Weight.Bold)
    lexer.setFont(keyword_font, QsciLexerJavaScript.Keyword)

    for style, color_key in [
        (QsciLexerJavaScript.Default, "default"),
        (QsciLexerJavaScript.Keyword, "keyword"),
        (QsciLexerJavaScript.Number, "numbers"),
        (QsciLexerJavaScript.DoubleQuotedString, "string"),
        (QsciLexerJavaScript.SingleQuotedString, "string2"),
        (QsciLexerJavaScript.Comment, "comment"),
        (QsciLexerJavaScript.CommentLine, "comment"),
        (QsciLexerJavaScript.CommentDoc, "comment"),
        (QsciLexerJavaScript.Identifier, "default"),
        (QsciLexerJavaScript.Operator, "operators"),
        (QsciLexerJavaScript.UnclosedString, "string"),
        (QsciLexerJavaScript.RegEx, "regex"),
        (QsciLexerJavaScript.CommentLineDoc, "comment"),
        (QsciLexerJavaScript.TemplateString, "string"),
    ]:
        lexer.setColor(QColor(color_schemes[color_key]), style)
