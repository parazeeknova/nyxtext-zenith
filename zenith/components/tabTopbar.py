from PyQt6.QtWidgets import QTabWidget
from ..scripts.color_scheme_loader import color_schemes


def tabRow(self, splitter):

    tabline_bg = color_schemes["tab_bg"]
    tabselect = color_schemes["tabselect"]
    tabline_bg_hover = color_schemes["tab_bg_hover"]

    self.tabWidget = QTabWidget()
    self.tabWidget.setStyleSheet(
        f"""
            QTabWidget::pane {{
                border-top: 2px solid {tabline_bg};
                margin: 0px;
            }}
            QTabBar::tab:selected {{
                border-bottom-color: {tabselect};
            }}
            QTabBar::tab {{
                background: {tabline_bg};
                color: white;
                margin-bottom: 2px;
                padding: 4px;
            }}
            QTabBar::tab:hover {{
                background: {tabline_bg_hover};
            }}
            QTabBar::tab:selected {{
                border-bottom: 2px solid {tabselect};
                border-bottom-color: {tabselect};
                background: {tabline_bg_hover};
                color: white;
            }}
            QTabBar::close-button {{
                subcontrol-position: right;
            }}
            """
    )
    self.tabWidget.setTabsClosable(True)
    self.tabWidget.tabCloseRequested.connect(self.closeTab)
    splitter.addWidget(self.tabWidget)
