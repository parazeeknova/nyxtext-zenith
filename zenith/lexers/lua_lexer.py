# lua_lexer.py
from PyQt6.Qsci import QsciLexerLua
from PyQt6.QtGui import QColor, QFont


def customize_lua_lexer(lexer, color_schemes):
    default_font = QFont("JetBrainsMono Nerd Font", 10)
    lexer.setFont(default_font)

    for style, color_key in [
        (QsciLexerLua.Default, "default"),
        (QsciLexerLua.Comment, "comment"),
        (QsciLexerLua.LineComment, "comment"),
        (QsciLexerLua.Number, "numbers"),
        (QsciLexerLua.Keyword, "keyword"),
        (QsciLexerLua.String, "string"),
        (QsciLexerLua.Character, "string2"),
        (QsciLexerLua.LiteralString, "lua_literal_string"),
        (QsciLexerLua.Preprocessor, "lua_preprocessor"),
        (QsciLexerLua.Operator, "operators"),
        (QsciLexerLua.Identifier, "default"),
        (QsciLexerLua.UnclosedString, "lua_unclosed_string"),
        (QsciLexerLua.BasicFunctions, "lua_basic_functions"),
        (QsciLexerLua.StringTableMathsFunctions, "lua_string_table_maths_functions"),
        (
            QsciLexerLua.CoroutinesIOSystemFacilities,
            "lua_coroutines_io_system_facilities",
        ),
        (QsciLexerLua.KeywordSet5, "lua_keyword_set5"),
        (QsciLexerLua.KeywordSet6, "lua_keyword_set6"),
        (QsciLexerLua.KeywordSet7, "lua_keyword_set7"),
        (QsciLexerLua.KeywordSet8, "lua_keyword_set8"),
        (QsciLexerLua.Label, "lua_label"),
    ]:
        lexer.setColor(QColor(color_schemes[color_key]), style)
