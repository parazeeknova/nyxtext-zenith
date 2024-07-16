from PyQt6.Qsci import QsciLexerCMake
from PyQt6.QtGui import QColor, QFont


def customize_cmake_lexer(lexer, color_schemes):
    default_font = QFont("JetBrainsMono Nerd Font", 10)
    lexer.setFont(default_font)

    for style, color_key in [
        (QsciLexerCMake.Default, "default"),
        (QsciLexerCMake.Comment, "comment"),
        (QsciLexerCMake.String, "string"),
        (QsciLexerCMake.StringLeftQuote, "cmake_string_left_quote"),
        (QsciLexerCMake.StringRightQuote, "cmake_string_right_quote"),
        (QsciLexerCMake.Function, "func"),
        (QsciLexerCMake.Variable, "cmake_variable"),
        (QsciLexerCMake.Label, "cmake_label"),
        (QsciLexerCMake.KeywordSet3, "cmake_keyword_set3"),
        (QsciLexerCMake.BlockWhile, "cmake_block_while"),
        (QsciLexerCMake.BlockForeach, "cmake_block_foreach"),
        (QsciLexerCMake.BlockIf, "cmake_block_if"),
        (QsciLexerCMake.BlockMacro, "cmake_block_macro"),
        (QsciLexerCMake.StringVariable, "cmake_string_variable"),
        (QsciLexerCMake.Number, "numbers"),
    ]:
        lexer.setColor(QColor(color_schemes[color_key]), style)
