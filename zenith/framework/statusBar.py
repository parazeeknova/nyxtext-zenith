from PySide6.QtWidgets import QPushButton, QStatusBar


class ZenithStatusBar(QStatusBar):
    def __init__(self, parent=None, zenithInstance=None):
        super().__init__(parent)
        self.zenithInstance = zenithInstance

        addTabButton = QPushButton("+", self)
        addTabButton.setStyleSheet(
            "background-color: transparent; border: none; padding-right: 5px;"
        )
        if self.zenithInstance:
            addTabButton.clicked.connect(self.zenithInstance.addNewTab)

        removeTabButton = QPushButton("-", self)
        removeTabButton.setStyleSheet(
            "background-color: transparent; border: none; padding-right: 5px;"
        )

        removeTabButton.clicked.connect(
            lambda: self.zenithInstance.tabWidget.removeTab(
                self.zenithInstance.tabWidget.currentIndex()
            )
        )

        self.addPermanentWidget(addTabButton)
        self.addPermanentWidget(removeTabButton)
        self.setStyleSheet(
            """
          QStatusBar::item {
              border: none;
          }
          QLabel {
              padding-left: 5px;
              padding-bottom: 5px;
          }
          """
        )
