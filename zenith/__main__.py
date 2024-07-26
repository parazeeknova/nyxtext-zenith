import argparse
import sys

from PyQt6.QtWidgets import QApplication

from .core.zenith_core import Zenith


def main():
    parser = argparse.ArgumentParser(description="Zenith Text Editor")
    parser.add_argument("-o", "--open", help="Open a specified file", metavar="FILE")

    args = parser.parse_args()

    app = QApplication(sys.argv)
    mainWindow = Zenith()

    if args.open:
        mainWindow.openDaemon.openFileFromTree(args.open)

    mainWindow.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
