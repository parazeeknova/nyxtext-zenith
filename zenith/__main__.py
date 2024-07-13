import sys

from PyQt6.QtWidgets import QApplication

from .zenith_core import Zenith


def main():
    try:
        app = QApplication(sys.argv)
        window = Zenith()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
