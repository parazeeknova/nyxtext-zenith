import logging

from PyQt6.Qsci import QsciScintilla
from PyQt6.QtCore import QObject
from PyQt6.QtGui import QColor


class LanguageFeatures(QObject):
    def __init__(self, codespace, color_schemes):
        super().__init__(codespace)
        self.codespace = codespace
        self.color_schemes = color_schemes

    def get_current_word(self):
        line, index = self.codespace.getCursorPosition()
        text = self.codespace.text(line)
        if not text:
            return ""

        word_end = min(index, len(text))
        while word_end < len(text) and (
            text[word_end].isalnum() or text[word_end] in "_"
        ):
            word_end += 1

        word_start = max(0, index - 1)
        while word_start > 0 and (
            text[word_start - 1].isalnum() or text[word_start - 1] in "_"
        ):
            word_start -= 1

        return text[word_start:word_end]

    def initialize(self):
        raise NotImplementedError("Subclasses must implement initialize method")

    def customize_lexer(self):
        raise NotImplementedError("Subclasses must implement customize_lexer method")

    def setup_autocompletion(self):
        raise NotImplementedError(
            "Subclasses must implement setup_autocompletion method"
        )

    def setup_calltips(self):
        raise NotImplementedError("Subclasses must implement setup_calltips method")

    def update_autocompletion(self):
        raise NotImplementedError(
            "Subclasses must implement update_autocompletion method"
        )

    def show_calltip(self):
        raise NotImplementedError("Subclasses must implement show_calltip method")

    def setup_calltip_style(self):
        try:
            self.codespace.setCallTipsBackgroundColor(
                QColor(self.color_schemes["calltip_bg"])
            )
            self.codespace.setCallTipsForegroundColor(
                QColor(self.color_schemes["calltip_fg"])
            )
            self.codespace.setCallTipsHighlightColor(
                QColor(self.color_schemes["calltip_highlight"])
            )
            self.codespace.setCallTipsStyle(QsciScintilla.CallTipsStyle.CallTipsContext)
            self.codespace.setCallTipsVisible(0)
            self.codespace.SendScintilla(
                QsciScintilla.SCI_CALLTIPUSESTYLE, 1
            )  # Enable HTML styling
            logging.info("Calltip style set up successfully")
        except Exception as e:
            logging.exception(f"Error setting up calltip style: {e}")
