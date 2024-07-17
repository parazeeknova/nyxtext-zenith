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

        # File icons based on file name
        file_name = file_info.fileName().lower()
        if file_name == "license":
            return self.license
        if file_name == "vercel.json":
            return self.vercel
        if file_name == "dockerfile":
            return self.docker
        if file_name == "gulpfile.js":
            return self.gulp
        if file_name == "package.json":
            return self.nodejs
        if file_name == "package-lock.json":
            return self.nodejs_alt
        if file_name in ["bun.lockb", "bun.lock", "bun"]:
            return self.bun

        # Folder icons based on folder name
        if file_info.isDir():
            if file_info.fileName() == ".github":
                return self.github_folder
            if file_info.fileName() in ["__pycache__", ".mypy_cache"]:
                return self.python_folder
            if file_info.fileName().lower() in ["scripts", "bin"]:
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
            if file_info.fileName() in ["utils", "utilities"]:
                return self.utils_folder
            if file_info.fileName() in ["src", "source"]:
                return self.src_folder
            if file_info.fileName().lower() in ["include", "includes"]:
                return self.include_folder
            if file_info.fileName().lower() in ["lib", "libs"]:
                return self.lib_folder
            if file_info.fileName() in ["app", "application"]:
                return self.folder_app
            if file_info.fileName() in ["pages", "views"]:
                return self.folder_pages
            if file_info.fileName() in ["css", "styles"]:
                return self.folder_css
            if file_info.fileName() in ["js", "javascript"]:
                return self.folder_js
            if file_info.fileName() in ["sass", "scss"]:
                return self.folder_sass
            if file_info.fileName() in ["node", "node_modules"]:
                return self.folder_node
            if file_info.fileName() in [
                "dist",
                "build",
                "bin",
                "out",
                "output",
                ".bin",
            ]:
                return self.folder_dist
            if file_info.fileName() in ["pdf", "pdfs"]:
                return self.folder_pdf
            if file_info.fileName() in ["fonts", "font"]:
                return self.folder_font
            if file_info.fileName() in ["resources", "res"]:
                return self.assets
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
        elif suffix in ["toml", "ini", "cfg", "conf", "flake8", "config"]:
            if file_info.fileName() == "pyproject.toml":
                return self.python_misc
            return self.config_icon
        elif suffix in ["bat", "cmd"]:
            return self.batch
        elif suffix == "exe":
            return self.exe
        elif suffix in ["yml", "yaml"]:
            if file_info.fileName() == "dependabot.yml":
                return self.dependabot
            return self.yaml
        elif suffix == "zip":
            return self.zip
        elif suffix == "sass":
            return self.sass
        elif suffix == "svg":
            return self.svg
        elif suffix in ["ttf", "otf", "woff", "woff2"]:
            return self.font

        return self.default_icon  # Default icon for unknown file types
