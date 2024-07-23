from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QStatusBar, QWidget

from ..scripts.color_scheme_loader import color_schemes


class Separator(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.VLine)
        self.setFrameShadow(QFrame.Shadow.Sunken)


class ZenithStatusBar(QStatusBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(
            f"""
            QStatusBar {{
                background-color: {color_schemes['statusbar_bg']};
                color: {color_schemes['statusbar_fg']};
                padding-bottom: 2px;
                position: absolute;
                bottom: 0;
            }}
            QStatusBar::item {{
                border: none;
            }}
            QLabel {{
                padding: 0 2px;
                color: {color_schemes['statusbar_fg']};
            }}
            """
        )

        self.lineLabel = QLabel("▼ Line:")
        self.lineValueLabel = QLabel("0")
        self.columnLabel = QLabel("▲ Column:")
        self.columnValueLabel = QLabel("0")
        self.totalLinesLabel = QLabel("∑ Total Lines:")
        self.totalLinesValueLabel = QLabel("0")
        self.wordsLabel = QLabel("⌁ Words:")
        self.wordsValueLabel = QLabel("0")

        self.encodingLabel = QLabel("UTF-8")
        self.lineEndingLabel = QLabel("LF")
        self.fileSizeLabel = QLabel("0 KB")

        smallFont = QFont()
        smallFont.setPointSize(8)

        for label in [
            self.lineLabel,
            self.columnLabel,
            self.totalLinesLabel,
            self.wordsLabel,
            self.encodingLabel,
            self.lineEndingLabel,
            self.fileSizeLabel,
        ]:
            label.setFont(smallFont)
            label.setStyleSheet(f"color: {color_schemes['statusbar_fg']};")

        for label in [
            self.lineValueLabel,
            self.columnValueLabel,
            self.totalLinesValueLabel,
            self.wordsValueLabel,
        ]:
            label.setFont(smallFont)
            label.setStyleSheet(f"color: {color_schemes['statusbar_fg']};")

        rightWidget = QWidget()
        rightLayout = QHBoxLayout(rightWidget)
        rightLayout.setContentsMargins(0, 0, 0, 5)
        rightLayout.setSpacing(1)

        rightLayout.addWidget(Separator())
        rightLayout.addWidget(self.lineLabel)
        rightLayout.addWidget(self.lineValueLabel)
        rightLayout.addWidget(Separator())
        rightLayout.addWidget(self.columnLabel)
        rightLayout.addWidget(self.columnValueLabel)
        rightLayout.addWidget(Separator())
        rightLayout.addWidget(self.totalLinesLabel)
        rightLayout.addWidget(self.totalLinesValueLabel)
        rightLayout.addWidget(Separator())
        rightLayout.addWidget(self.wordsLabel)
        rightLayout.addWidget(self.wordsValueLabel)
        rightLayout.addWidget(Separator())

        rightLayout.addWidget(self.encodingLabel)
        rightLayout.addWidget(Separator())
        rightLayout.addWidget(self.lineEndingLabel)
        rightLayout.addWidget(Separator())
        rightLayout.addWidget(self.fileSizeLabel)

        self.addPermanentWidget(rightWidget)

        self.lexerLabel = QLabel("Lexer: None")
        self.lexerLabel.setFont(smallFont)
        self.lexerLabel.setStyleSheet(f"color: {color_schemes['statusbar_fg']};")
        rightLayout.addWidget(self.lexerLabel)
        rightLayout.addWidget(Separator())

        self.editModeLabel = QLabel("ReadOnly")
        self.editModeLabel.setFont(smallFont)
        self.editModeLabel.setStyleSheet(
            f"""
            color: {color_schemes['statusbar_fg']};
            font-weight: bold;
            margin-bottom: 5px;
            """
        )

        self.addWidget(self.editModeLabel)

    def updateStats(self, line, column, total_lines, words):
        self.lineValueLabel.setText(str(line))
        self.columnValueLabel.setText(str(column))
        self.totalLinesValueLabel.setText(str(total_lines))
        self.wordsValueLabel.setText(str(words))

    def updateLexer(self, lexerName):
        self.lexerLabel.setText(f"Lexer: {lexerName}")

    def showLexerLoadingMessage(self):
        self.showMessage("Lexers are loading, please wait...", 5000)

    def updateEncoding(self, encoding):
        self.encodingLabel.setText(encoding)

    def updateLineEnding(self, lineEnding):
        self.lineEndingLabel.setText(lineEnding)

    def updateFileSize(self, size):
        self.fileSizeLabel.setText(f"{size:.2f} KB")

    def updateEditMode(self, mode):
        self.editModeLabel.setText(mode)
        if mode == "ReadOnly":
            self.editModeLabel.setStyleSheet(
                f"color: {color_schemes['editmode_readonly']};"
            )
        else:
            self.editModeLabel.setStyleSheet(
                f"color: {color_schemes['editmode_edit']};"
            )
