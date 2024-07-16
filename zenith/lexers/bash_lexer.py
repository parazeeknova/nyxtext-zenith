from PyQt6.Qsci import QsciLexerBash
from PyQt6.QtGui import QColor, QFont


def customize_bash_lexer(lexer, color_schemes):
    default_font = QFont("JetBrainsMono Nerd Font", 10)
    lexer.setFont(default_font)

    for style, color_key in [
        (QsciLexerBash.Default, "default"),
        (QsciLexerBash.Error, "bash_error"),
        (QsciLexerBash.Comment, "comment"),
        (QsciLexerBash.Number, "numbers"),
        (QsciLexerBash.Keyword, "keyword"),
        (QsciLexerBash.DoubleQuotedString, "string"),
        (QsciLexerBash.SingleQuotedString, "string2"),
        (QsciLexerBash.Operator, "operators"),
        (QsciLexerBash.Identifier, "bash_identifier"),
        (QsciLexerBash.Scalar, "bash_scalar"),
        (QsciLexerBash.ParameterExpansion, "bash_parameter_expansion"),
        (QsciLexerBash.Backticks, "bash_backticks"),
        (QsciLexerBash.HereDocumentDelimiter, "bash_here_document_delimiter"),
        (QsciLexerBash.SingleQuotedHereDocument, "bash_single_quoted_here_document"),
    ]:
        lexer.setColor(QColor(color_schemes[color_key]), style)
