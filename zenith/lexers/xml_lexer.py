from PyQt6.Qsci import QsciLexerXML
from PyQt6.QtGui import QColor, QFont


def customize_xml_lexer(lexer, color_schemes):
    default_font = QFont("JetBrainsMono Nerd Font", 10)
    lexer.setFont(default_font)

    for style, color_key in [
        (QsciLexerXML.Default, "default"),
        (QsciLexerXML.Tag, "xml_tag"),
        (QsciLexerXML.UnknownTag, "xml_unknown_tag"),
        (QsciLexerXML.Attribute, "xml_attribute"),
        (QsciLexerXML.UnknownAttribute, "xml_unknown_attribute"),
        (QsciLexerXML.Number, "numbers"),
        (QsciLexerXML.DoubleQuotedString, "string"),
        (QsciLexerXML.SingleQuotedString, "string2"),
        (QsciLexerXML.OtherInTag, "xml_other_in_tag"),
        (QsciLexerXML.Comment, "comment"),
        (QsciLexerXML.Entity, "xml_entity"),
        (QsciLexerXML.TagEnd, "xml_tag_end"),
        (QsciLexerXML.XMLStart, "xml_start"),
        (QsciLexerXML.XMLEnd, "xml_end"),
        (QsciLexerXML.Script, "xml_script"),
        (QsciLexerXML.CDATA, "xml_cdata"),
        (QsciLexerXML.Question, "xml_question"),
        (QsciLexerXML.Value, "xml_value"),
    ]:
        lexer.setColor(QColor(color_schemes[color_key]), style)
