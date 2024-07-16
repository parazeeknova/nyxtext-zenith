from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFileSystemModel, QIcon

from ..media.icon_resources import icon_resources
from ..scripts.def_path import resource

folder = resource(r"../media/filetree/folder.png")

resources = {
    icon_name: resource(
        r"../media/filetree/{}.{}".format(
            file_type, "svg" if file_type != "folder" else "png"
        )
    )
    for icon_name, file_type in icon_resources.items()
}


class CustomFileSystemModel(QFileSystemModel):
    def __init__(self, parent=None):
        super().__init__(parent)

        for icon_name in icon_resources:
            setattr(self, icon_name, QIcon(resources[icon_name]))

        self.folder_icon = QIcon(folder)

    def data(self, index, role):
        if role == Qt.ItemDataRole.DecorationRole:
            file_info = self.fileInfo(index)
            return self.getCustomIcon(file_info)
        return super().data(index, role)

    def getCustomIcon(self, file_info):

        # Folder icons based on folder name
        if file_info.isDir():
            if file_info.fileName() == ".github":
                return self.github_folder
            if file_info.fileName() in ["__pycache__", ".mypy_cache"]:
                return self.python_folder
            if file_info.fileName() == "scripts":
                return self.scripts_folder
            if file_info.fileName() in [
                ".venv",
                "env",
                "venv",
                "virtualenv",
                "envs",
                "venvs",
                ".env",
            ]:
                return self.environment_folder
            if file_info.fileName() == ".git":
                return self.git_folder
            if file_info.fileName() == "zenith":
                return self.zenith
            if file_info.fileName() == "workflows":
                return self.github_workflow
            if file_info.fileName() == "assets":
                return self.assets
            if file_info.fileName() == "misc":
                return self.misc
            if file_info.fileName() == "svg":
                return self.svg_folder
            if file_info.fileName() in [
                "images",
                "img",
                "pictures",
                "pics",
                "photos",
                "screenshots",
                "screenshot",
                "media",
            ]:
                return self.images_folder
            if file_info.fileName() in ["components", "comps"]:
                return self.components_folder
            if file_info.fileName() in ["core", "src"]:
                return self.core_folder
            if file_info.fileName() in ["framework", "tools"]:
                return self.framework_folder
            if file_info.fileName() in ["lexer", "syntax", "lexers"]:
                return self.lexer_folder
            return self.folder_icon  # Default folder icon for unknown folder names

        # File icons based on file extension or name
        suffix = file_info.suffix().lower()
        if suffix in ["py", "pyc", "pyo", "pyw", "pyz"]:
            if file_info.fileName() == "__init__.py":
                return self.python_misc
            return self.python_icon
        elif suffix in ["lua", "luac"]:
            return self.lua_icon
        elif suffix in ["html", "htm"]:
            return self.html_icon
        elif suffix == "css":
            return self.css_icon
        elif suffix == "js":
            return self.javascript_icon
        elif suffix == "json":
            return self.json_icon
        elif suffix in ["jpg", "jpeg", "png", "gif", "bmp", "tiff"]:
            return self.image_icon
        elif suffix == "gitignore":
            return self.git_icon
        elif suffix == "git":
            return self.git_icon
        elif suffix == "md":
            if file_info.fileName().lower() == "readme.md":
                return self.readme
            if file_info.fileName().lower() == "security.md":
                return self.security
            if file_info.fileName().lower() == "code_of_conduct.md":
                return self.conduct
            if file_info.fileName().lower() == "contributing.md":
                return self.contributing
            return self.markdown_icon
        elif suffix == "txt":
            if file_info.fileName() == "requirements.txt":
                return self.python_misc
            return self.default_icon
        elif suffix in ["toml", "ini", "cfg", "conf", "flake8"]:
            if file_info.fileName() == "pyproject.toml":
                return self.python_misc
            return self.config_icon
        elif suffix in ["bat", "cmd"]:
            return self.batch
        elif suffix in ["yml", "yaml"]:
            if file_info.fileName() == "dependabot.yml":
                return self.dependabot
            return self.yaml
        return self.default_icon  # Default icon for unknown file types
