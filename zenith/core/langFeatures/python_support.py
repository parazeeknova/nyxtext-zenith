import logging

import jedi  # type: ignore
from PyQt6.Qsci import QsciAPIs, QsciLexerPython, QsciScintilla
from PyQt6.QtCore import QMetaObject, QObject, Qt, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QColor, QFont

logging.basicConfig(
    level=logging.DEBUG,
    filename="zenith_debug.log",
    filemode="w",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


class PythonFeatures(QObject):
    updateRequired = pyqtSignal()

    def __init__(self, codespace, color_schemes):
        super().__init__(codespace)
        self.codespace = codespace
        self.color_schemes = color_schemes
        self.api = None
        QMetaObject.invokeMethod(self, "initialize", Qt.ConnectionType.QueuedConnection)

    @pyqtSlot()
    def initialize(self):
        try:
            self.customize_lexer()
            self.api = QsciAPIs(self.codespace.lexer())
            self.setup_autocompletion()
            self.setup_calltips()
            logging.info("PythonFeatures initialized successfully")
        except Exception as e:
            logging.exception(f"Error initializing PythonFeatures: {e}")

    def customize_lexer(self):
        try:
            lexer = QsciLexerPython(self.codespace)
            self.codespace.setLexer(lexer)

            default_font = QFont("JetBrainsMono Nerd Font", 10)
            lexer.setFont(default_font)

            comment_font = QFont("JetBrainsMono Nerd Font", 10, italic=True)
            lexer.setFont(comment_font, QsciLexerPython.Comment)

            keyword_font = QFont(
                "JetBrainsMono Nerd Font", 10, weight=QFont.Weight.Bold
            )
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
                lexer.setColor(QColor(self.color_schemes[color_key]), style)

            # Explicitly set margin colors
            self.codespace.setMarginsForegroundColor(
                QColor(self.color_schemes["margin_fg"])
            )
            self.codespace.setMarginsBackgroundColor(
                QColor(self.color_schemes["margin_bg"])
            )

            logging.info("Python lexer customized successfully")
        except Exception as e:
            logging.exception(f"Error customizing Python lexer: {e}")

    def setup_autocompletion(self):
        if not self.api:
            logging.error("API is None, cannot set up autocompletion")
            return
        try:
            self.codespace.setAutoCompletionSource(
                QsciScintilla.AutoCompletionSource.AcsAPIs
            )
            self.codespace.setAutoCompletionThreshold(1)
            self.codespace.setAutoCompletionCaseSensitivity(False)
            self.codespace.setAutoCompletionReplaceWord(False)
            self.codespace.setAutoCompletionUseSingle(
                QsciScintilla.AutoCompletionUseSingle.AcusNever
            )

            for word in self.get_python_keywords():
                self.api.add(word)

            self.api.prepare()
            self.codespace.textChanged.connect(self.update_autocompletion)
            logging.info("Autocompletion set up successfully")
        except Exception as e:
            logging.exception(f"Error setting up autocompletion: {e}")

    def setup_calltips(self):
        try:
            self.codespace.setCallTipsStyle(QsciScintilla.CallTipsStyle.CallTipsContext)
            self.codespace.setCallTipsVisible(0)
            self.codespace.callTipsStyle()
            self.codespace.cursorPositionChanged.connect(self.show_calltip)
            logging.info("Calltips set up successfully")
        except Exception as e:
            logging.exception(f"Error setting up calltips: {e}")

    def update_autocompletion(self):
        try:
            script = jedi.Script(
                code=self.codespace.text(), path=self.codespace.file_path
            )
            completions = script.complete(
                line=self.codespace.getCursorPosition()[0] + 1,
                column=self.codespace.getCursorPosition()[1],
            )

            self.api.clear()
            for completion in completions:
                self.api.add(completion.name)

            self.api.prepare()
            self.updateRequired.emit()
            logging.debug(f"Autocompletion updated with {len(completions)} completions")
        except Exception as e:
            logging.exception(f"Error updating autocompletion: {e}")

    def show_calltip(self):
        try:
            script = jedi.Script(
                code=self.codespace.text(), path=self.codespace.file_path
            )
            signatures = script.get_signatures(
                line=self.codespace.getCursorPosition()[0] + 1,
                column=self.codespace.getCursorPosition()[1],
            )

            if signatures:
                signature = signatures[0]
                calltip = f"{signature.name}({', '.join(param.name for param in signature.params)})"
                self.codespace.callTip(
                    self.codespace.positionFromLineIndex(
                        *self.codespace.getCursorPosition()
                    ),
                    calltip,
                )
                logging.debug(f"Calltip shown: {calltip}")
            else:
                logging.debug("No calltip available at current position")
        except Exception as e:
            logging.exception(f"Error showing calltip: {e}")

    def get_python_keywords(self):
        return [
            "False",
            "None",
            "True",
            "print",
            "and",
            "as",
            "assert",
            "break",
            "class",
            "continue",
            "def",
            "del",
            "elif",
            "else",
            "except",
            "finally",
            "for",
            "from",
            "global",
            "if",
            "import",
            "in",
            "is",
            "lambda",
            "nonlocal",
            "not",
            "or",
            "pass",
            "raise",
            "return",
            "try",
            "while",
            "with",
            "yield",
        ]
