import os
import sys

from PySide6.QtWidgets import QApplication

from .zenith_core import Zenith

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Zenith()
    window.show()
    sys.exit(app.exec())
