# css_lexer.py
from PyQt6.Qsci import QsciLexerCSS
from PyQt6.QtGui import QColor, QFont


def customize_css_lexer(lexer, color_schemes):
    default_font = QFont("JetBrainsMono Nerd Font", 10)
    lexer.setFont(default_font)

    for style, color_key in [
        (QsciLexerCSS.Default, "default"),
        (QsciLexerCSS.Tag, "css_tag"),
        (QsciLexerCSS.ClassSelector, "css_class"),
        (QsciLexerCSS.PseudoClass, "css_pseudo_class"),
        (QsciLexerCSS.UnknownPseudoClass, "css_unknown_pseudo_class"),
        (QsciLexerCSS.Operator, "operators"),
        (QsciLexerCSS.CSS1Property, "css_property"),
        (QsciLexerCSS.UnknownProperty, "css_unknown_property"),
        (QsciLexerCSS.Value, "css_value"),
        (QsciLexerCSS.Comment, "comment"),
        (QsciLexerCSS.IDSelector, "css_id_selector"),
        (QsciLexerCSS.Important, "css_important"),
        (QsciLexerCSS.AtRule, "css_at_rule"),
        (QsciLexerCSS.DoubleQuotedString, "string"),
        (QsciLexerCSS.SingleQuotedString, "string2"),
        (QsciLexerCSS.CSS2Property, "css_property"),
        (QsciLexerCSS.Attribute, "css_attribute"),
        (QsciLexerCSS.CSS3Property, "css_property"),
        (QsciLexerCSS.PseudoElement, "css_pseudo_element"),
        (QsciLexerCSS.ExtendedCSSProperty, "css_extended_property"),
        (QsciLexerCSS.ExtendedPseudoClass, "css_extended_pseudo_class"),
        (QsciLexerCSS.ExtendedPseudoElement, "css_extended_pseudo_element"),
    ]:
        lexer.setColor(QColor(color_schemes[color_key]), style)
