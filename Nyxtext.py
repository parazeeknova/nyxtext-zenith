import argparse
import sys

from PyQt6.QtWidgets import QApplication

from zenith.zenith_core import Zenith


def Nyxtext():
    parser = argparse.ArgumentParser(description="Nyx Text Editor")
    parser.add_argument("-o", "--open", help="Open a specified file", metavar="FILE")

    args = parser.parse_args()

    app = QApplication(sys.argv)
    Nyxtext = Zenith()

    if args.open:
        Nyxtext.openFileFromTree(args.open)

    Nyxtext.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    Nyxtext()
