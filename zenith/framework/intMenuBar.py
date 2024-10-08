from lupa import LuaError, LuaRuntime  # type: ignore
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QMenuBar, QMessageBox

from ..components.codeSpace import Codespace
from ..scripts.color_scheme_loader import color_schemes

lua = LuaRuntime(unpack_returned_tuples=True)


def menu_bar(self, zenithInstance=None):
    menuBar = QMenuBar(self)
    fileMenu = menuBar.addMenu("File")
    editMenu = menuBar.addMenu("Edit")
    selectMenu = menuBar.addMenu("Search")
    viewMenu = menuBar.addMenu("View")
    settingsMenu = menuBar.addMenu("Settings")
    runMenu = menuBar.addMenu("Run")
    terminalMenu = menuBar.addMenu("Terminal")
    helpMenu = menuBar.addMenu("Help")

    menuBar.setStyleSheet(
        f"""
        QMenuBar {{
            background-color: {color_schemes['menubar_bg']};
            color: {color_schemes['menubar_fg']};
            font-size: 12px;
            spacing: 0px;
        }}
        QMenuBar::item {{
            background-color: transparent;
            padding: 5px;
        }}
        QMenuBar::item:selected {{
            background-color: {color_schemes['menubar_selected']};
        }}
        QMenu {{
            background-color: {color_schemes['menu_bg']};
            color: {color_schemes['menu_fg']};
            font-size: 12px;
            font-weight: bold;
            spacing: 0px;
        }}
        QMenu::item {{
            background-color: transparent;
            padding: 2px 15px 2px 15px;
            margin: 2px 5px 5px 5px;
        }}
        QMenu::item:selected {{
            background-color: {color_schemes['menu_selected']};
        }}
        QMenu::separator {{
            height: 1px;
            background: {color_schemes['menu_separator']};
            margin-left: 10px;
            margin-right: 10px;
        }}
        """
    )

    try:
        filepath = r"zenith/shortcuts.lua"
        with open(filepath, "r") as file:
            lua_code = file.read()
        shortcuts = lua.execute(lua_code)

        newWorkspaceTabAction = QAction("New Workspace Tab", self)
        newWorkspaceTabAction.setShortcut(shortcuts["new_tab"])
        newWorkspaceTabAction.triggered.connect(lambda: self.parent().addNewTab())
        fileMenu.addAction(newWorkspaceTabAction)

        newCodespaceAction = QAction("New Codespace", self)
        newCodespaceAction.setShortcut(shortcuts["codespace"])
        newCodespaceAction.triggered.connect(
            lambda: Codespace(zenithInstance.tabWidget)
        )
        fileMenu.addAction(newCodespaceAction)

        fileMenu.addSeparator()

        openAction = QAction("Open", self)
        openAction.setShortcut(shortcuts["open"])
        if zenithInstance and hasattr(zenithInstance, "openDaemon"):
            openAction.triggered.connect(zenithInstance.openDaemon.openFile)
        else:
            openAction.triggered.connect(
                lambda: QMessageBox.warning(
                    self, "Error", "Open file functionality not available"
                )
            )
        fileMenu.addAction(openAction)

        openFolderAction = QAction("Open Folder", self)
        openFolderAction.setShortcut(shortcuts["open_folder"])
        if zenithInstance and hasattr(zenithInstance, "openDaemon"):
            openFolderAction.triggered.connect(zenithInstance.openDaemon.openFolder)
        else:
            openFolderAction.triggered.connect(
                lambda: QMessageBox.warning(
                    self, "Error", "Open folder functionality not available"
                )
            )
        fileMenu.addAction(openFolderAction)

        fileMenu.addSeparator()

        saveAction = QAction("Save", self)
        saveAction.setShortcut(shortcuts["save"])
        if zenithInstance and hasattr(zenithInstance, "saveDaemon"):
            saveAction.triggered.connect(zenithInstance.saveDaemon.saveFile)
        else:
            saveAction.triggered.connect(
                lambda: QMessageBox.warning(
                    self, "Error", "Save file functionality not available"
                )
            )
        fileMenu.addAction(saveAction)

        saveAsAction = QAction("Save As", self)
        saveAsAction.setShortcut(shortcuts["save_as"])
        if zenithInstance and hasattr(zenithInstance, "saveDaemon"):
            saveAsAction.triggered.connect(zenithInstance.saveDaemon.saveFileAs)
        else:
            saveAsAction.triggered.connect(
                lambda: QMessageBox.warning(
                    self, "Error", "Save file as functionality not available"
                )
            )
        fileMenu.addAction(saveAsAction)

        fileMenu.addAction("Save All")
        fileMenu.addSeparator()

        closeTabAction = QAction("Close Tab", self)
        closeTabAction.setShortcut(shortcuts["close_tab"])
        closeTabAction.triggered.connect(
            lambda: zenithInstance.closeTab(zenithInstance.tabWidget.currentIndex())
        )
        fileMenu.addAction(closeTabAction)

        closeAllTabsAction = QAction("Close All Tabs", self)
        closeAllTabsAction.setShortcut(shortcuts["close_all_tabs"])
        closeAllTabsAction.triggered.connect(zenithInstance.closeAllTabs)
        fileMenu.addAction(closeAllTabsAction)

        fileMenu.addSeparator()

        exitAction = QAction("Exit", self)
        exitAction.setShortcut(shortcuts["exit"])
        exitAction.triggered.connect(QApplication.instance().quit)
        fileMenu.addAction(exitAction)

        editMenu.addAction("Undo")
        editMenu.addAction("Redo")

        return menuBar

    except LuaError as e:
        QMessageBox.warning(self, "Error", f"Error executing Lua script: {e}")
    except FileNotFoundError:
        QMessageBox.warning(self, "Error", f"Shortcuts file not found: {filepath}")
    except Exception as e:
        QMessageBox.warning(self, "Error", f"An unexpected error occurred: {e}")

    return menuBar
