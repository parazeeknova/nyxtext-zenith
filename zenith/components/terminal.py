import os
import re
import subprocess

from PyQt6.QtCore import QProcess, Qt, pyqtSignal
from PyQt6.QtGui import QColor, QIcon, QKeyEvent, QTextCursor
from PyQt6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class TerminalEmulator(QWidget):
    commandEntered = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.setup_toolbar()

        self.terminal = QPlainTextEdit(self)
        self.terminal.setStyleSheet(
            """
            QPlainTextEdit {
                background-color: #1E1E1E;
                color: white;
                font-family: Consolas, Courier, monospace;
            }
        """
        )
        self.terminal.keyPressEvent = self.terminal_key_press_event

        self.layout.addWidget(self.terminal)

        self.processes = []
        self.current_process_index = -1

        self.command_history = []
        self.history_index = 0

        self.addNewTab()

    def setup_toolbar(self):
        toolbar = QWidget()
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(5, 0, 5, 0)

        self.terminal_selector = QComboBox()
        self.terminal_selector.setStyleSheet("QComboBox { min-width: 150px; }")
        self.terminal_selector.currentIndexChanged.connect(self.switchTab)

        new_terminal_button = QPushButton(QIcon("path/to/new_icon.png"), "")
        new_terminal_button.setToolTip("New Terminal")
        new_terminal_button.clicked.connect(self.addNewTab)

        kill_terminal_button = QPushButton(QIcon("path/to/kill_icon.png"), "")
        kill_terminal_button.setToolTip("Kill Terminal")
        kill_terminal_button.clicked.connect(self.killCurrentTerminal)

        toolbar_layout.addWidget(self.terminal_selector)
        toolbar_layout.addWidget(new_terminal_button)
        toolbar_layout.addWidget(kill_terminal_button)
        toolbar_layout.addStretch()

        self.layout.addWidget(toolbar)

    def addNewTab(self):
        index = self.terminal_selector.count()
        self.terminal_selector.addItem(f"Terminal {index + 1}")
        process = QProcess(self)
        process.readyReadStandardOutput.connect(self.handle_stdout)
        process.readyReadStandardError.connect(self.handle_stderr)
        self.processes.append(process)
        self.terminal_selector.setCurrentIndex(index)
        self.start_powershell(index)

    def killCurrentTerminal(self):
        if self.current_process_index >= 0:
            self.processes[self.current_process_index].kill()
            self.terminal_selector.removeItem(self.current_process_index)
            del self.processes[self.current_process_index]
            if self.terminal_selector.count() == 0:
                self.addNewTab()
            else:
                self.current_process_index = self.terminal_selector.currentIndex()

    def switchTab(self, index):
        self.current_process_index = index
        self.terminal.clear()
        self.terminal.appendPlainText("> ")

    def closeTab(self, index):
        if self.tabBar.count() > 1:
            self.processes[index].kill()
            del self.processes[index]
            self.tabBar.removeTab(index)
            if index == self.current_process_index:
                self.current_process_index = self.tabBar.currentIndex()

    def start_powershell(self, index):
        powershell_path = self.find_powershell_core()
        if powershell_path:
            self.processes[index].start(powershell_path)
            self.terminal.appendPlainText(
                f"""PowerShell Core started at {powershell_path}.
                Type your commands below.\n"""
            )
        else:
            self.terminal.appendPlainText(
                "PowerShell Core not found. Using default PowerShell.\n"
            )
            self.processes[index].start("powershell.exe")

        self.terminal.appendPlainText("> ")

    def find_powershell_core(self):
        possible_paths = [
            r"C:\Program Files\PowerShell\7\pwsh.exe",
            r"C:\Program Files (x86)\PowerShell\7\pwsh.exe",
            "/usr/local/bin/pwsh",
            "/usr/bin/pwsh",
        ]

        for path in possible_paths:
            if os.path.exists(path):
                return path
        try:
            result = subprocess.run(
                ["where", "pwsh"] if os.name == "nt" else ["which", "pwsh"],
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return None

    def handle_stdout(self):
        data = (
            self.processes[self.current_process_index]
            .readAllStandardOutput()
            .data()
            .decode()
        )
        self.terminal.moveCursor(QTextCursor.MoveOperation.End)
        self.insert_colored_text(data)
        if not data.endswith("\n"):
            self.terminal.insertPlainText("\n")
        self.terminal.moveCursor(QTextCursor.MoveOperation.End)

    def handle_stderr(self):
        data = (
            self.processes[self.current_process_index]
            .readAllStandardError()
            .data()
            .decode()
        )
        self.terminal.moveCursor(QTextCursor.MoveOperation.End)
        self.insert_colored_text(data, QColor(255, 0, 0))  # Red color for errors
        if not data.endswith("\n"):
            self.terminal.insertPlainText("\n")
        self.terminal.moveCursor(QTextCursor.MoveOperation.End)

    def insert_colored_text(self, text, default_color=QColor(255, 255, 255)):
        cursor = self.terminal.textCursor()

        ansi_escape = re.compile(r"\x1B\[[0-9;]*m")
        segments = ansi_escape.split(text)
        codes = ansi_escape.findall(text)

        current_color = default_color
        for i, segment in enumerate(segments):
            if segment:
                format = cursor.charFormat()
                format.setForeground(current_color)
                cursor.setCharFormat(format)
                cursor.insertText(segment)

            if i < len(codes):
                code = codes[i]
                if code == "\x1B[0m":  # Reset
                    current_color = default_color
                elif code.startswith("\x1B[38;2;"):  # RGB color
                    rgb = code[7:-1].split(";")
                    if len(rgb) == 3:
                        current_color = QColor(int(rgb[0]), int(rgb[1]), int(rgb[2]))

        self.terminal.setTextCursor(cursor)

    def keyPressEvent(self, event: QKeyEvent | None):
        if event is not None:
            if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
                self.execute_command()
            elif event.key() == Qt.Key.Key_Up:
                self.show_previous_command()
            elif event.key() == Qt.Key.Key_Down:
                self.show_next_command()
            else:
                super().keyPressEvent(event)

    def terminal_key_press_event(self, event: QKeyEvent):
        cursor = self.terminal.textCursor()

        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            self.execute_command()
        elif event.key() == Qt.Key.Key_Backspace:
            if cursor.positionInBlock() > 2:  # Allow backspace only after prompt
                cursor.deletePreviousChar()
        elif event.key() == Qt.Key.Key_Up:
            self.show_previous_command()
        elif event.key() == Qt.Key.Key_Down:
            self.show_next_command()
        elif event.key() == Qt.Key.Key_Left:
            if cursor.positionInBlock() > 2:  # Don't move left of prompt
                cursor.movePosition(QTextCursor.MoveOperation.Left)
        elif event.key() == Qt.Key.Key_Home:
            cursor.movePosition(QTextCursor.MoveOperation.StartOfLine)
            cursor.movePosition(
                QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.MoveAnchor, 2
            )
        else:
            if cursor.positionInBlock() < 2:  # Don't allow editing prompt
                cursor.movePosition(QTextCursor.MoveOperation.EndOfLine)
            QPlainTextEdit.keyPressEvent(self.terminal, event)

    def execute_command(self):
        cursor = self.terminal.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.EndOfBlock)
        cursor.movePosition(
            QTextCursor.MoveOperation.StartOfBlock, QTextCursor.MoveMode.KeepAnchor
        )
        line = cursor.selectedText()

        if line.startswith("> "):
            command = line[2:]
            self.terminal.appendPlainText("")
            self.processes[self.current_process_index].write(command.encode() + b"\n")
            self.command_history.append(command)
            self.history_index = len(self.command_history)
            self.commandEntered.emit(command)
        else:
            # If the line doesn't start with "> ", it's likely a colorful prompt
            # In this case, just execute whatever is after the prompt
            command = line.split()[-1]  # Get the last word as the command
            self.terminal.appendPlainText("")
            self.processes[self.current_process_index].write(command.encode() + b"\n")
            self.command_history.append(command)
            self.history_index = len(self.command_history)
            self.commandEntered.emit(command)

    def show_previous_command(self):
        if self.history_index > 0:
            self.history_index -= 1
            self.show_command_from_history()

    def show_next_command(self):
        if self.history_index < len(self.command_history) - 1:
            self.history_index += 1
            self.show_command_from_history()
        elif self.history_index == len(self.command_history) - 1:
            self.history_index += 1
            self.show_command_from_history()

    def show_command_from_history(self):
        cursor = self.terminal.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.EndOfBlock)
        cursor.movePosition(
            QTextCursor.MoveOperation.StartOfBlock, QTextCursor.MoveMode.KeepAnchor
        )
        cursor.removeSelectedText()

        if self.history_index < len(self.command_history):
            command = self.command_history[self.history_index]
            cursor.insertText(f"> {command}")
        else:
            cursor.insertText("> ")

    def run_command(self, command):
        self.terminal.moveCursor(QTextCursor.MoveOperation.End)
        self.terminal.insertPlainText(f"> {command}\n")
        self.processes[self.current_process_index].write(command.encode() + b"\n")

    def run_file(self, file_path):
        file_type = os.path.splitext(file_path)[1]
        if file_type == ".py":
            self.run_command(f"python {file_path}")
        elif file_type == ".js":
            self.run_command(f"node {file_path}")

    def change_directory(self, new_path):
        self.run_command(f"cd '{new_path}'")

    def parse_ansi_codes(self, text):
        ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
        return ansi_escape.sub("", text)
