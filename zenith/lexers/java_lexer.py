from PyQt6.Qsci import QsciLexerJava
from PyQt6.QtGui import QColor, QFont


def customize_java_lexer(lexer, color_schemes):
    default_font = QFont("JetBrainsMono Nerd Font", 10)
    lexer.setFont(default_font)

    for style, color_key in [
        (QsciLexerJava.Default, "default"),
        (QsciLexerJava.Keyword, "keyword"),
        (QsciLexerJava.Number, "numbers"),
        (QsciLexerJava.String, "string"),
        (QsciLexerJava.Character, "string2"),
        (QsciLexerJava.Operator, "operators"),
        (QsciLexerJava.Identifier, "java_identifier"),
        (QsciLexerJava.JavaDoc, "java_javadoc"),
        (QsciLexerJava.Comment, "comment"),
        (QsciLexerJava.CommentLine, "comment"),
        (QsciLexerJava.CommentDoc, "java_javadoc"),
        (QsciLexerJava.CommentLineDoc, "java_javadoc"),
        (QsciLexerJava.JavaDocKeyword, "java_javadoc_keyword"),
    ]:
        lexer.setColor(QColor(color_schemes[color_key]), style)
