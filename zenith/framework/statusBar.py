from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QStatusBar, QWidget


class Separator(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.VLine)
        self.setFrameShadow(QFrame.Shadow.Sunken)


class ZenithStatusBar(QStatusBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(
            """
            QStatusBar {
                padding-bottom: 2px;
            }
            QStatusBar::item {
                border: none;
            }
            QLabel {
                padding: 0 2px;
            }
        """
        )

        self.readyLabel = QLabel("READY")
        self.readyLabel.setStyleSheet(
            "color: #a6da95; font-weight: bold; margin-bottom: 5px;"
        )
        self.lineLabel = QLabel("▼ Line:")
        self.lineValueLabel = QLabel("0")
        self.columnLabel = QLabel("▲ Column:")
        self.columnValueLabel = QLabel("0")
        self.totalLinesLabel = QLabel("∑ Total Lines:")
        self.totalLinesValueLabel = QLabel("0")
        self.wordsLabel = QLabel("⌁ Words:")
        self.wordsValueLabel = QLabel("0")

        smallFont = QFont()
        smallFont.setPointSize(8)

        for label in [
            self.lineLabel,
            self.columnLabel,
            self.totalLinesLabel,
            self.wordsLabel,
        ]:
            label.setFont(smallFont)
            label.setStyleSheet("color: #cad3f5;")

        for label in [
            self.lineValueLabel,
            self.columnValueLabel,
            self.totalLinesValueLabel,
            self.wordsValueLabel,
        ]:
            label.setFont(smallFont)
            label.setStyleSheet("color: #cad3f5;")

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

        self.addPermanentWidget(rightWidget)
        self.addWidget(self.readyLabel)

        self.lexerLabel = QLabel("Lexer: None")
        self.lexerLabel.setFont(smallFont)
        self.lexerLabel.setStyleSheet("color: #cad3f5;")
        rightLayout.addWidget(self.lexerLabel)
        rightLayout.addWidget(Separator())

    def showMessage(self, message, timeout=0):
        super().showMessage(message, timeout)
        self.readyLabel.setVisible(not bool(message))

    def updateStats(self, line, column, total_lines, words):
        self.lineValueLabel.setText(str(line))
        self.columnValueLabel.setText(str(column))
        self.totalLinesValueLabel.setText(str(total_lines))
        self.wordsValueLabel.setText(str(words))

    def updateLexer(self, lexerName):
        self.lexerLabel.setText(f"Lexer: {lexerName}")
