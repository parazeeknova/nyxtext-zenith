# md_lexer.py
from PyQt6.Qsci import QsciLexerMarkdown
from PyQt6.QtGui import QColor, QFont


def customize_md_lexer(lexer, color_schemes):
    default_font = QFont("JetBrainsMono Nerd Font", 10)
    lexer.setFont(default_font)

    for style, color_key in [
        (QsciLexerMarkdown.Default, "md_default"),
        (QsciLexerMarkdown.Special, "md_default"),
        (QsciLexerMarkdown.StrongEmphasis1, "md_strong"),
        (QsciLexerMarkdown.StrongEmphasis2, "md_strong"),
        (QsciLexerMarkdown.StrongEmphasis3, "md_strong"),
        (QsciLexerMarkdown.Emphasis1, "md_emphasis"),
        (QsciLexerMarkdown.Emphasis2, "md_emphasis"),
        (QsciLexerMarkdown.Emphasis3, "md_emphasis"),
        (QsciLexerMarkdown.Header1, "md_header"),
        (QsciLexerMarkdown.Header2, "md_header"),
        (QsciLexerMarkdown.Header3, "md_header"),
        (QsciLexerMarkdown.Header4, "md_header"),
        (QsciLexerMarkdown.Header5, "md_header"),
        (QsciLexerMarkdown.Header6, "md_header"),
        (QsciLexerMarkdown.Prechar, "md_list_item"),
        (QsciLexerMarkdown.UnorderedListItem, "md_list_item"),
        (QsciLexerMarkdown.OrderedListItem, "md_list_item"),
        (QsciLexerMarkdown.BlockQuote, "md_blockquote"),
        (QsciLexerMarkdown.StrikeOut, "md_emphasis"),
        (QsciLexerMarkdown.HorizontalRule, "md_horizontal_rule"),
        (QsciLexerMarkdown.Link, "md_link"),
        (QsciLexerMarkdown.CodeBackticks, "md_code"),
        (QsciLexerMarkdown.CodeDoubleBackticks, "md_code"),
        (QsciLexerMarkdown.CodeBlock, "md_code_block"),
    ]:
        lexer.setColor(QColor(color_schemes[color_key]), style)

    # Set background color for code blocks
    lexer.setPaper(
        QColor(color_schemes["md_code_block_bg"]), QsciLexerMarkdown.CodeBlock
    )
