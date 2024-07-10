from PyQt6.QtWidgets import QTabWidget


def tabRow(self, splitter):
    self.tabWidget = QTabWidget()
    self.tabWidget.setStyleSheet(
        """
            QTabWidget::pane {
                border-top: 2px solid #333;
                margin: 0px;
            }
            QTabBar::tab:selected {
                border-bottom-color: #C2C7CB;
            }
            QTabBar::tab {
                background: #333;
                border-radius: 2px;
                color: white;
                margin-bottom: 2px;
                padding: 4px;
            }
            QTabBar::tab:hover {
                background: #444;
            }
            QTabBar::tab:selected {
                border-bottom: 2px solid #C2C7CB;
                border-bottom-color: #C2C7CB;
                background: #444;
                color: white;
            }
            QTabBar::close-button {
                subcontrol-position: right;
            }
            """
    )
    self.tabWidget.setTabsClosable(True)
    self.tabWidget.tabCloseRequested.connect(self.closeTab)
    splitter.addWidget(self.tabWidget)
