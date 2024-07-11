from lupa import LuaError, LuaRuntime
from PyQt6.QtGui import QKeySequence, QShortcut
from PyQt6.QtWidgets import QMessageBox

lua = LuaRuntime(unpack_returned_tuples=True)


def key_shortcuts(main_window):
    filepath = r"zenith\shortcuts.lua"

    try:
        with open(filepath, "r") as file:
            lua_code = file.read()
        shortcuts = lua.execute(lua_code)

        toggle_file_tree_shortcut = QShortcut(
            QKeySequence(shortcuts["toggle_file_tree"]), main_window
        )
        toggle_file_tree_shortcut.activated.connect(
            main_window.fileTree.toggleFileTreeVisibility
        )

        next_tab_shortcut = QShortcut(QKeySequence(shortcuts["next_tab"]), main_window)
        next_tab_shortcut.activated.connect(main_window.nextTab)

        prev_tab_shortcut = QShortcut(QKeySequence(shortcuts["prev_tab"]), main_window)
        prev_tab_shortcut.activated.connect(main_window.prevTab)

    except LuaError as e:
        QMessageBox.warning(main_window, "Error", f"Error executing Lua script: {e}")
    except FileNotFoundError:
        QMessageBox.warning(
            main_window, "Error", f"Shortcuts file not found: {filepath}"
        )
    except Exception as e:
        QMessageBox.warning(main_window, "Error", f"An unexpected error occurred: {e}")
