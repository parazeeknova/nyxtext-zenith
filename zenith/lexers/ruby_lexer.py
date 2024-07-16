from PyQt6.Qsci import QsciLexerRuby
from PyQt6.QtGui import QColor, QFont


def customize_ruby_lexer(lexer, color_schemes):
    default_font = QFont("JetBrainsMono Nerd Font", 10)
    lexer.setFont(default_font)

    for style, color_key in [
        (QsciLexerRuby.Default, "default"),
        (QsciLexerRuby.Error, "ruby_error"),
        (QsciLexerRuby.Comment, "comment"),
        (QsciLexerRuby.POD, "ruby_pod"),
        (QsciLexerRuby.Number, "numbers"),
        (QsciLexerRuby.Keyword, "keyword"),
        (QsciLexerRuby.DoubleQuotedString, "string"),
        (QsciLexerRuby.SingleQuotedString, "string2"),
        (QsciLexerRuby.ClassName, "class"),
        (QsciLexerRuby.FunctionMethodName, "func"),
        (QsciLexerRuby.Operator, "operators"),
        (QsciLexerRuby.Identifier, "ruby_identifier"),
        (QsciLexerRuby.Regex, "regex"),
        (QsciLexerRuby.Global, "ruby_global"),
        (QsciLexerRuby.Symbol, "ruby_symbol"),
        (QsciLexerRuby.ModuleName, "ruby_module_name"),
        (QsciLexerRuby.InstanceVariable, "ruby_instance_variable"),
        (QsciLexerRuby.ClassVariable, "ruby_class_variable"),
        (QsciLexerRuby.BacktickHereDocument, "ruby_backtick_here_document"),
        (QsciLexerRuby.HereDocument, "ruby_here_document"),
        (QsciLexerRuby.PercentStringq, "ruby_percent_string_q"),
        (QsciLexerRuby.PercentStringQ, "ruby_percent_string_Q"),
    ]:
        lexer.setColor(QColor(color_schemes[color_key]), style)
