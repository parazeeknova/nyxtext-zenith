import sys

from PyQt6.QtWidgets import QApplication

from zenith.zenith_core import Zenith

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Zenith()
    window.show()
    sys.exit(app.exec())
	