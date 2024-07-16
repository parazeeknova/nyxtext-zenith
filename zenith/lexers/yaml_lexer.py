from PyQt6.Qsci import QsciLexerYAML
from PyQt6.QtGui import QColor, QFont


def customize_yaml_lexer(lexer, color_schemes):
    default_font = QFont("JetBrainsMono Nerd Font", 10)
    lexer.setFont(default_font)

    for style, color_key in [
        (QsciLexerYAML.Default, "default"),
        (QsciLexerYAML.Comment, "comment"),
        (QsciLexerYAML.Identifier, "yaml_identifier"),
        (QsciLexerYAML.Keyword, "keyword"),
        (QsciLexerYAML.Number, "numbers"),
        (QsciLexerYAML.Reference, "yaml_reference"),
        (QsciLexerYAML.DocumentDelimiter, "yaml_document_delimiter"),
        (QsciLexerYAML.TextBlockMarker, "yaml_text_block_marker"),
        (QsciLexerYAML.SyntaxErrorMarker, "yaml_syntax_error_marker"),
        (QsciLexerYAML.Operator, "operators"),
    ]:
        lexer.setColor(QColor(color_schemes[color_key]), style)
