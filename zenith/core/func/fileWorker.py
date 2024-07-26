from PyQt6.QtCore import Q_ARG, QMetaObject, QObject, QRunnable, Qt, pyqtSignal


class FileWorker(QRunnable):
    class Signals(QObject):
        finished = pyqtSignal(str, str)
        error = pyqtSignal(str)

    def __init__(self, file_path, content=None, mode="r"):
        super().__init__()
        self.file_path = file_path
        self.content = content
        self.mode = mode
        self.signals = self.Signals()

    def run(self):
        try:
            if self.mode == "r":
                with open(self.file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                QMetaObject.invokeMethod(
                    self.signals,
                    "finished",
                    Qt.ConnectionType.QueuedConnection,
                    Q_ARG(str, self.file_path),
                    Q_ARG(str, content),
                )
            elif self.mode == "w":
                with open(self.file_path, "w", encoding="utf-8") as file:
                    file.write(self.content)
                QMetaObject.invokeMethod(
                    self.signals,
                    "finished",
                    Qt.ConnectionType.QueuedConnection,
                    Q_ARG(str, self.file_path),
                    Q_ARG(str, ""),
                )
        except Exception as e:
            QMetaObject.invokeMethod(
                self.signals,
                "error",
                Qt.ConnectionType.QueuedConnection,
                Q_ARG(str, str(e)),
            )
