from PyQt6.Qsci import QsciLexerBatch
from PyQt6.QtGui import QColor, QFont


def customize_batch_lexer(lexer, color_schemes):
    default_font = QFont("JetBrainsMono Nerd Font", 10)
    lexer.setFont(default_font)

    for style, color_key in [
        (QsciLexerBatch.Default, "default"),
        (QsciLexerBatch.Comment, "comment"),
        (QsciLexerBatch.Keyword, "keyword"),
        (QsciLexerBatch.Label, "batch_label"),
        (QsciLexerBatch.HideCommandChar, "batch_hide_command_char"),
        (QsciLexerBatch.ExternalCommand, "batch_external_command"),
        (QsciLexerBatch.Variable, "batch_variable"),
        (QsciLexerBatch.Operator, "operators"),
    ]:
        lexer.setColor(QColor(color_schemes[color_key]), style)
