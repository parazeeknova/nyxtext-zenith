import json

from PySide6.QtGui import QKeySequence, QShortcut


def key_shortcuts(main_window):

    filepath = "zenith\\shortcuts.json"
    with open(filepath, "r") as file:
        shortcuts = json.load(file)

    new_tab_shortcut = QShortcut(QKeySequence(shortcuts["new_tab"]), main_window)
    new_tab_shortcut.activated.connect(main_window.addNewTab)

    close_tab_shortcut = QShortcut(QKeySequence(shortcuts["close_tab"]), main_window)
    close_tab_shortcut.activated.connect(
        lambda: main_window.closeTab(main_window.tabWidget.currentIndex())
    )
