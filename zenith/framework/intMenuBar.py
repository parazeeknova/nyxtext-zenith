from PyQt6.QtWidgets import QMenuBar


def menu_bar(parent):
    menuBar = QMenuBar(parent)
    fileMenu = menuBar.addMenu("File")
    editMenu = menuBar.addMenu("Edit")
    selectMenu = menuBar.addMenu("Select")
    viewMenu = menuBar.addMenu("View")
    goMenu = menuBar.addMenu("Go")
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
        }
        QMenu::item {
            background-color: transparent;
        }
        QMenu::item:selected {
            background-color: #2d2d2d;
        }
    """
    )

    fileMenu.addAction("New")
    fileMenu.addAction("Open")
    fileMenu.addAction("Save")
    editMenu.addAction("Undo")
    editMenu.addAction("Redo")

    return menuBar
