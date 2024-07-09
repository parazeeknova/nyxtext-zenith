import json

from PyQt6.QtGui import QKeySequence, QShortcut
from PyQt6.QtWidgets import QMessageBox


def key_shortcuts(main_window):
    filepath = r"zenith\shortcuts.json"

    try:
        with open(filepath, "r") as file:
            shortcuts = json.load(file)

        new_tab_shortcut = QShortcut(QKeySequence(shortcuts["new_tab"]), main_window)
        new_tab_shortcut.activated.connect(main_window.addNewTab)

        close_tab_shortcut = QShortcut(
            QKeySequence(shortcuts["close_tab"]), main_window
        )
        close_tab_shortcut.activated.connect(
            lambda: main_window.closeTab(main_window.tabWidget.currentIndex())
        )

        toggle_file_tree_shortcut = QShortcut(
            QKeySequence(shortcuts["toggle_file_tree"]), main_window
        )
        toggle_file_tree_shortcut.activated.connect(
            main_window.fileTree.toggleFileTreeVisibility
        )

    except FileNotFoundError:
        QMessageBox.warning(
            main_window, "Error", f"Shortcuts file not found: {filepath}"
        )
    except json.JSONDecodeError:
        QMessageBox.warning(
            main_window, "Error", "Invalid JSON format in shortcuts file."
        )
    except KeyError as e:
        QMessageBox.warning(main_window, "Error", f"Missing key in shortcuts file: {e}")
