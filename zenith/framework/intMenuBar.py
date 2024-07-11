from lupa import LuaError, LuaRuntime  # type: ignore
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QFileDialog, QMenuBar, QMessageBox

from ..components.codeSpace import Codespace

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
        """
        QMenuBar {
            background-color: #1e1e1e;
            color: #cad3f5;
            font-size: 12px;
            spacing: 0px;
        }
        QMenuBar::item {
            background-color: transparent;
            padding: 5px;
        }
        QMenuBar::item:selected {
            background-color: #2d2d2d;
        }
        QMenu {
            background-color: #1e1e1e;
            color: #cad3f5;
            font-size: 12px;
            font-weight: bold;
            spacing: 0px;
        }
        QMenu::item {
            background-color: transparent;
            padding: 2px 15px 2px 15px;
            margin: 2px 5px 5px 5px;
        }
        QMenu::item:selected {
            background-color: #2d2d2d;
        }
        QMenu::separator {
        height: 1px;
        background: 	#5b6078;
        margin-left: 10px;
        margin-right: 10px;
        }
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
        openAction.triggered.connect(lambda: self.parent().openFile())
        fileMenu.addAction(openAction)

        openFolderAction = QAction("Open Folder", self)
        openFolderAction.setShortcut(shortcuts["open_folder"])
        openFolderAction.triggered.connect(zenithInstance.openFolder)
        fileMenu.addAction(openFolderAction)

        fileMenu.addSeparator()

        saveAction = QAction("Save", self)
        saveAction.setShortcut(shortcuts["save"])
        saveAction.triggered.connect(lambda: self.parent().saveFile())
        fileMenu.addAction(saveAction)

        saveAsAction = QAction("Save As", self)
        saveAsAction.setShortcut(shortcuts["save_as"])
        saveAsAction.triggered.connect(lambda: self.parent().saveFileAs())
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
