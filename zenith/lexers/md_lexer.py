# md_lexer.py
from PyQt6.Qsci import QsciLexerMarkdown
from PyQt6.QtGui import QColor, QFont


def customize_md_lexer(lexer, color_schemes):
    default_font = QFont("JetBrainsMono Nerd Font", 10)
    lexer.setFont(default_font)

    for style, color_key in [
        (QsciLexerMarkdown.Default, "default"),
        (QsciLexerMarkdown.Special, "md_special"),
        (QsciLexerMarkdown.StrongEmphasis1, "md_strong_emphasis"),
        (QsciLexerMarkdown.StrongEmphasis2, "md_strong_emphasis"),
        (QsciLexerMarkdown.Emphasis1, "md_emphasis"),
        (QsciLexerMarkdown.Emphasis2, "md_emphasis"),
        (QsciLexerMarkdown.Header1, "md_header1"),
        (QsciLexerMarkdown.Header2, "md_header2"),
        (QsciLexerMarkdown.Header3, "md_header3"),
        (QsciLexerMarkdown.Header4, "md_header4"),
        (QsciLexerMarkdown.Header5, "md_header5"),
        (QsciLexerMarkdown.Header6, "md_header6"),
        (QsciLexerMarkdown.Prechar, "md_prechar"),
        (QsciLexerMarkdown.UnorderedListItem, "md_unordered_list_item"),
        (QsciLexerMarkdown.OrderedListItem, "md_ordered_list_item"),
        (QsciLexerMarkdown.BlockQuote, "md_block_quote"),
        (QsciLexerMarkdown.StrikeOut, "md_strikeout"),
        (QsciLexerMarkdown.HorizontalRule, "md_horizontal_rule"),
        (QsciLexerMarkdown.Link, "md_link"),
        (QsciLexerMarkdown.CodeBackticks, "md_code_backticks"),
        (QsciLexerMarkdown.CodeBlock, "md_code_block"),
        (QsciLexerMarkdown.CodeFence1, "md_code_fence"),
        (QsciLexerMarkdown.CodeFence2, "md_code_fence"),
        (QsciLexerMarkdown.CodeFence3, "md_code_fence"),
    ]:
        lexer.setColor(QColor(color_schemes[color_key]), style)
