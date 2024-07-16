from PyQt6.Qsci import QsciLexerProperties
from PyQt6.QtGui import QColor, QFont


def customize_properties_lexer(lexer, color_schemes):
    default_font = QFont("JetBrainsMono Nerd Font", 10)
    lexer.setFont(default_font)

    for style, color_key in [
        (QsciLexerProperties.Default, "prop_default"),
        (QsciLexerProperties.Key, "prop_key"),
        (QsciLexerProperties.Section, "prop_section"),
        (QsciLexerProperties.Assignment, "prop_assignment"),
        (QsciLexerProperties.DefaultValue, "prop_value"),
        (QsciLexerProperties.Comment, "prop_comment"),
    ]:
        lexer.setColor(QColor(color_schemes[color_key]), style)
