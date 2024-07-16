from PyQt6.Qsci import QsciLexerCPP
from PyQt6.QtGui import QColor, QFont


def customize_cpp_lexer(lexer, color_schemes):
    default_font = QFont("JetBrainsMono Nerd Font", 10)
    lexer.setFont(default_font)

    for style, color_key in [
        (QsciLexerCPP.Default, "default"),
        (QsciLexerCPP.Comment, "comment"),
        (QsciLexerCPP.CommentLine, "comment"),
        (QsciLexerCPP.CommentDoc, "c_comment_doc"),
        (QsciLexerCPP.Number, "numbers"),
        (QsciLexerCPP.Keyword, "keyword"),
        (QsciLexerCPP.DoubleQuotedString, "string"),
        (QsciLexerCPP.SingleQuotedString, "string2"),
        (QsciLexerCPP.UUID, "c_uuid"),
        (QsciLexerCPP.PreProcessor, "c_preprocessor"),
        (QsciLexerCPP.Operator, "operators"),
        (QsciLexerCPP.Identifier, "c_identifier"),
        (QsciLexerCPP.UnclosedString, "c_unclosed_string"),
        (QsciLexerCPP.VerbatimString, "c_verbatim_string"),
        (QsciLexerCPP.Regex, "regex"),
        (QsciLexerCPP.CommentLineDoc, "c_comment_line_doc"),
        (QsciLexerCPP.KeywordSet2, "c_keyword_set2"),
        (QsciLexerCPP.CommentDocKeyword, "c_comment_doc_keyword"),
        (QsciLexerCPP.CommentDocKeywordError, "c_comment_doc_keyword_error"),
        (QsciLexerCPP.GlobalClass, "c_global_class"),
        (QsciLexerCPP.RawString, "c_raw_string"),
        (QsciLexerCPP.TripleQuotedVerbatimString, "c_triple_quoted_verbatim_string"),
        (QsciLexerCPP.HashQuotedString, "c_hash_quoted_string"),
        (QsciLexerCPP.PreProcessorComment, "c_preprocessor_comment"),
        (QsciLexerCPP.PreProcessorCommentLineDoc, "c_preprocessor_comment_line_doc"),
    ]:
        lexer.setColor(QColor(color_schemes[color_key]), style)
