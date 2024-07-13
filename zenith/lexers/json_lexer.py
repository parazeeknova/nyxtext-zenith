# json_lexer.py
from PyQt6.Qsci import QsciLexerJSON
from PyQt6.QtGui import QColor, QFont


def customize_json_lexer(lexer, color_schemes):
    default_font = QFont("JetBrainsMono Nerd Font", 10)
    lexer.setFont(default_font)

    for style, color_key in [
        (QsciLexerJSON.Default, "default"),
        (QsciLexerJSON.Number, "numbers"),
        (QsciLexerJSON.String, "string"),
        (QsciLexerJSON.UnclosedString, "json_unclosed_string"),
        (QsciLexerJSON.Property, "json_property"),
        (QsciLexerJSON.EscapeSequence, "json_escape_sequence"),
        (QsciLexerJSON.LineComment, "comment"),
        (QsciLexerJSON.BlockComment, "comment"),
        (QsciLexerJSON.Operator, "operators"),
        (QsciLexerJSON.IRI, "json_iri"),
        (QsciLexerJSON.IRICompact, "json_iri_compact"),
        (QsciLexerJSON.Keyword, "keyword"),
        (QsciLexerJSON.KeywordLD, "json_keyword_ld"),
        (QsciLexerJSON.Error, "json_error"),
    ]:
        lexer.setColor(QColor(color_schemes[color_key]), style)
