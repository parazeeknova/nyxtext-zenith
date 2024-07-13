# html_lexer.py
from PyQt6.Qsci import QsciLexerHTML
from PyQt6.QtGui import QColor, QFont


def customize_html_lexer(lexer, color_schemes):
    default_font = QFont("JetBrainsMono Nerd Font", 10)
    lexer.setFont(default_font)

    for style, color_key in [
        (QsciLexerHTML.Default, "default"),
        (QsciLexerHTML.Tag, "html_tag"),
        (QsciLexerHTML.UnknownTag, "html_unknown_tag"),
        (QsciLexerHTML.Attribute, "html_attribute"),
        (QsciLexerHTML.UnknownAttribute, "html_unknown_attribute"),
        (QsciLexerHTML.HTMLNumber, "numbers"),
        (QsciLexerHTML.HTMLDoubleQuotedString, "string"),
        (QsciLexerHTML.HTMLSingleQuotedString, "string2"),
        (QsciLexerHTML.OtherInTag, "html_other_in_tag"),
        (QsciLexerHTML.HTMLComment, "comment"),
        (QsciLexerHTML.Entity, "html_entity"),
        (QsciLexerHTML.XMLTagEnd, "html_tag_end"),
        (QsciLexerHTML.XMLStart, "html_xml_start"),
        (QsciLexerHTML.XMLEnd, "html_xml_end"),
        (QsciLexerHTML.Script, "html_script"),
        (QsciLexerHTML.ASPAtStart, "html_asp_at_start"),
        (QsciLexerHTML.ASPStart, "html_asp_start"),
        (QsciLexerHTML.CDATA, "html_cdata"),
        (QsciLexerHTML.PHPStart, "html_php_start"),
        (QsciLexerHTML.HTMLValue, "html_value"),
    ]:
        lexer.setColor(QColor(color_schemes[color_key]), style)
