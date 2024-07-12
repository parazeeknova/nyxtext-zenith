from lupa import LuaRuntime  # type: ignore
from PyQt6.QtWidgets import QMessageBox, QTabWidget

lua = LuaRuntime(unpack_returned_tuples=True)


def tabRow(self, splitter):

    scheme = r"zenith\color_schemes.lua"
    try:
        with open(scheme, "r") as file:
            lua_code = file.read()
        color_schemes = lua.execute(lua_code)
    except FileNotFoundError:
        QMessageBox.warning(None, "Error", "Color schemes file not found.")
        return
    except Exception as e:
        QMessageBox.warning(None, "Error", f"An unexpected error occurred: {e}")
        return

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
