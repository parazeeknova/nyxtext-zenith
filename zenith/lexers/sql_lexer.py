from PyQt6.Qsci import QsciLexerSQL
from PyQt6.QtGui import QColor, QFont


def customize_sql_lexer(lexer, color_schemes):
    default_font = QFont("JetBrainsMono Nerd Font", 10)
    lexer.setFont(default_font)

    for style, color_key in [
        (QsciLexerSQL.Default, "default"),
        (QsciLexerSQL.Comment, "comment"),
        (QsciLexerSQL.CommentLine, "comment"),
        (QsciLexerSQL.CommentDoc, "sql_comment_doc"),
        (QsciLexerSQL.Number, "numbers"),
        (QsciLexerSQL.Keyword, "keyword"),
        (QsciLexerSQL.DoubleQuotedString, "string"),
        (QsciLexerSQL.SingleQuotedString, "string2"),
        (QsciLexerSQL.PlusKeyword, "sql_plus_keyword"),
        (QsciLexerSQL.PlusPrompt, "sql_plus_prompt"),
        (QsciLexerSQL.Operator, "operators"),
        (QsciLexerSQL.Identifier, "sql_identifier"),
        (QsciLexerSQL.SQLPlus, "sql_plus"),
        (QsciLexerSQL.SQLPlusCommand, "sql_plus_command"),
        (QsciLexerSQL.QuotedIdentifier, "sql_quoted_identifier"),
        (QsciLexerSQL.QOperator, "sql_q_operator"),
    ]:
        lexer.setColor(QColor(color_schemes[color_key]), style)
