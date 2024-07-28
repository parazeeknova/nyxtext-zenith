import os

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QTabWidget

from ..scripts.color_scheme_loader import color_schemes


def resource(relative_path):
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up two levels to reach the project root
    project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
    # Join the project root with the relative path
    full_path = os.path.normpath(os.path.join(project_root, relative_path))
    # Convert to forward slashes for Qt
    qt_path = full_path.replace("\\", "/")
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"Resource not found: {full_path}")
    return qt_path


close_icon = resource(r"zenith/media/tab_manager/close.svg")


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
            image: url({close_icon});
            subcontrol-position: right;
        }}
        QTabBar::close-button:hover {{
            background: rgba(255, 255, 255, 0.1);
        }}
        """
    )
    self.tabWidget.setTabsClosable(True)
    self.tabWidget.tabCloseRequested.connect(self.closeTab)
    splitter.addWidget(self.tabWidget)

    # Customize tab bar
    tab_bar = self.tabWidget.tabBar()
    tab_bar.setIconSize(QSize(16, 16))
    tab_bar.setExpanding(False)
    tab_bar.setDrawBase(False)
    tab_bar.setElideMode(Qt.TextElideMode.ElideRight)

    return self.tabWidget
