from PyQt6.Qsci import QsciLexerPerl
from PyQt6.QtGui import QColor, QFont


def customize_perl_lexer(lexer, color_schemes):
    default_font = QFont("JetBrainsMono Nerd Font", 10)
    lexer.setFont(default_font)

    for style, color_key in [
        (QsciLexerPerl.Default, "default"),
        (QsciLexerPerl.Error, "perl_error"),
        (QsciLexerPerl.Comment, "comment"),
        (QsciLexerPerl.POD, "perl_pod"),
        (QsciLexerPerl.Number, "numbers"),
        (QsciLexerPerl.Keyword, "keyword"),
        (QsciLexerPerl.DoubleQuotedString, "string"),
        (QsciLexerPerl.SingleQuotedString, "string2"),
        (QsciLexerPerl.Operator, "operators"),
        (QsciLexerPerl.Identifier, "perl_identifier"),
        (QsciLexerPerl.Scalar, "perl_scalar"),
        (QsciLexerPerl.Array, "perl_array"),
        (QsciLexerPerl.Hash, "perl_hash"),
        (QsciLexerPerl.SymbolTable, "perl_symbol_table"),
        (QsciLexerPerl.Regex, "regex"),
        (QsciLexerPerl.Substitution, "perl_substitution"),
        (QsciLexerPerl.BacktickHereDocument, "perl_backtick_here_document"),
        (QsciLexerPerl.QuotedStringQ, "perl_quoted_string_q"),
        (QsciLexerPerl.QuotedStringQQ, "perl_quoted_string_qq"),
        (QsciLexerPerl.QuotedStringQX, "perl_quoted_string_qx"),
        (QsciLexerPerl.QuotedStringQR, "perl_quoted_string_qr"),
        (QsciLexerPerl.QuotedStringQW, "perl_quoted_string_qw"),
        (QsciLexerPerl.PODVerbatim, "perl_pod_verbatim"),
        (QsciLexerPerl.SubroutinePrototype, "perl_subroutine_prototype"),
        (QsciLexerPerl.FormatIdentifier, "perl_format_identifier"),
        (QsciLexerPerl.FormatBody, "perl_format_body"),
    ]:
        lexer.setColor(QColor(color_schemes[color_key]), style)
