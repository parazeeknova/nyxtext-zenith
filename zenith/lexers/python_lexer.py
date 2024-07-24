import logging
from PyQt6.Qsci import QsciLexerPython
from PyQt6.QtGui import QColor, QFont

def customize_python_lexer(lexer, color_schemes):
    try:
        default_font = QFont("JetBrainsMono Nerd Font", 10)
        lexer.setFont(default_font)

        comment_font = QFont("JetBrainsMono Nerd Font", 10, italic=True)
        lexer.setFont(comment_font, QsciLexerPython.Comment)

        keyword_font = QFont("JetBrainsMono Nerd Font", 10, weight=QFont.Weight.Bold)
        lexer.setFont(keyword_font, QsciLexerPython.Keyword)

        number_font = QFont("JetBrainsMono Nerd Font", 10, weight=QFont.Weight.Bold)
        lexer.setFont(number_font, QsciLexerPython.Number)

        for style, color_key in [
            (QsciLexerPython.Default, "default"),
            (QsciLexerPython.Keyword, "keyword"),
            (QsciLexerPython.Number, "numbers"),
            (QsciLexerPython.DoubleQuotedString, "string"),
            (QsciLexerPython.SingleQuotedString, "string2"),
            (QsciLexerPython.TripleSingleQuotedString, "string"),
            (QsciLexerPython.TripleDoubleQuotedString, "string2"),
            (QsciLexerPython.Comment, "comment"),
            (QsciLexerPython.CommentBlock, "comment"),
            (QsciLexerPython.Identifier, "default"),
            (QsciLexerPython.Operator, "operators"),
            (QsciLexerPython.FunctionMethodName, "func"),
            (QsciLexerPython.ClassName, "class"),
            (QsciLexerPython.Decorator, "keyword"),
        ]:
            lexer.setColor(QColor(color_schemes[color_key]), style)
        
        logging.info("Python lexer customized successfully")
    except Exception as e:
        logging.exception(f"Error customizing Python lexer: {e}")