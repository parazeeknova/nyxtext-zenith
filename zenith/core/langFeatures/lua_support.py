# flake8: noqa: E501
import logging
from typing import List

from PyQt6.Qsci import QsciAPIs, QsciLexerLua, QsciScintilla
from PyQt6.QtCore import QMetaObject, Qt, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QColor, QFont

from .language_features import LanguageFeatures

logging.basicConfig(
    level=logging.DEBUG,
    filename="zenith_debug.log",
    filemode="w",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


class LuaFeatures(LanguageFeatures):
    updateRequired = pyqtSignal()

    def __init__(self, codespace, color_schemes):
        super().__init__(codespace, color_schemes)
        self.api = None
        QMetaObject.invokeMethod(self, "initialize", Qt.ConnectionType.QueuedConnection)

    @pyqtSlot()
    def initialize(self):
        try:
            self.customize_lexer()
            self.api = QsciAPIs(self.codespace.lexer())
            self.setup_autocompletion()
            self.setup_calltips()
            logging.info("LuaFeatures initialized successfully")
        except Exception as e:
            logging.exception(f"Error initializing LuaFeatures: {e}")

    def customize_lexer(self):
        try:
            lexer = QsciLexerLua(self.codespace)
            self.codespace.setLexer(lexer)

            default_font = QFont("JetBrainsMono Nerd Font", 10)
            lexer.setFont(default_font)

            comment_font = QFont("JetBrainsMono Nerd Font", 10, italic=True)
            lexer.setFont(comment_font, QsciLexerLua.Comment)
            lexer.setFont(comment_font, QsciLexerLua.LineComment)

            keyword_font = QFont(
                "JetBrainsMono Nerd Font", 10, weight=QFont.Weight.Bold
            )
            lexer.setFont(keyword_font, QsciLexerLua.Keyword)

            number_font = QFont("JetBrainsMono Nerd Font", 10, weight=QFont.Weight.Bold)
            lexer.setFont(number_font, QsciLexerLua.Number)

            for style, color_key in [
                (QsciLexerLua.Default, "default"),
                (QsciLexerLua.Comment, "comment"),
                (QsciLexerLua.LineComment, "comment"),
                (QsciLexerLua.Number, "numbers"),
                (QsciLexerLua.Keyword, "keyword"),
                (QsciLexerLua.String, "string"),
                (QsciLexerLua.Character, "string2"),
                (QsciLexerLua.LiteralString, "lua_literal_string"),
                (QsciLexerLua.Preprocessor, "lua_preprocessor"),
                (QsciLexerLua.Operator, "operators"),
                (QsciLexerLua.Identifier, "default"),
                (QsciLexerLua.UnclosedString, "lua_unclosed_string"),
                (QsciLexerLua.BasicFunctions, "lua_basic_functions"),
                (
                    QsciLexerLua.StringTableMathsFunctions,
                    "lua_string_table_maths_functions",
                ),
                (
                    QsciLexerLua.CoroutinesIOSystemFacilities,
                    "lua_coroutines_io_system_facilities",
                ),
                (QsciLexerLua.KeywordSet5, "lua_keyword_set5"),
                (QsciLexerLua.KeywordSet6, "lua_keyword_set6"),
                (QsciLexerLua.KeywordSet7, "lua_keyword_set7"),
                (QsciLexerLua.KeywordSet8, "lua_keyword_set8"),
                (QsciLexerLua.Label, "lua_label"),
            ]:
                lexer.setColor(QColor(self.color_schemes[color_key]), style)

            self.codespace.setMarginsForegroundColor(
                QColor(self.color_schemes["margin_fg"])
            )
            self.codespace.setMarginsBackgroundColor(
                QColor(self.color_schemes["margin_bg"])
            )

            logging.info("Lua lexer customized successfully")
        except Exception as e:
            logging.exception(f"Error customizing Lua lexer: {e}")

    def setup_autocompletion(self):
        if not self.api:
            logging.error("API is None, cannot set up autocompletion")
            return
        try:
            self.codespace.setAutoCompletionSource(
                QsciScintilla.AutoCompletionSource.AcsAPIs
            )
            self.codespace.setAutoCompletionThreshold(1)
            self.codespace.setAutoCompletionCaseSensitivity(False)
            self.codespace.setAutoCompletionReplaceWord(False)
            self.codespace.setAutoCompletionUseSingle(
                QsciScintilla.AutoCompletionUseSingle.AcusNever
            )

            for keyword in self.get_lua_keywords():
                word, description = keyword.split("|")
                self.api.add(f"{word} - {description}")

            self.api.prepare()
            self.codespace.textChanged.connect(self.update_autocompletion)
            logging.info("Autocompletion set up successfully")
        except Exception as e:
            logging.exception(f"Error setting up autocompletion: {e}")

    def setup_calltips(self):
        try:
            LanguageFeatures.setup_calltip_style(self)
            self.codespace.cursorPositionChanged.connect(self.show_calltip)
            logging.info("Calltips set up successfully")
        except Exception as e:
            logging.exception(f"Error setting up calltips: {e}")

    def update_autocompletion(self):
        try:
            self.api.clear()
            current_word = self.get_current_word()
            for keyword in self.get_lua_keywords():
                word, description = keyword.split("|")
                if word.startswith(current_word):
                    self.api.add(f"{word} - {description}")

            # Add type-specific method completions
            if current_word:
                type_methods = {
                    "string": [
                        kw for kw in self.get_lua_keywords() if kw.startswith("string.")
                    ],
                    "table": [
                        kw for kw in self.get_lua_keywords() if kw.startswith("table.")
                    ],
                    "math": [
                        kw for kw in self.get_lua_keywords() if kw.startswith("math.")
                    ],
                }

                for type_name, methods in type_methods.items():
                    if current_word.endswith(f"{type_name}."):
                        for method in methods:
                            word, description = method.split("|")
                            self.api.add(f"{word[len(type_name)+1:]} - {description}")

            self.api.prepare()
            self.updateRequired.emit()
            logging.debug(f"Autocompletion updated for word: {current_word}")
        except Exception as e:
            logging.exception(f"Error updating autocompletion: {e}")

    def show_calltip(self):
        try:
            current_word = LanguageFeatures.get_current_word(self)
            for keyword in self.get_lua_keywords():
                word, description = keyword.split("|")
                if word.startswith(current_word):
                    function_name, params = word.split("(", 1)
                    params = params.rstrip(")")
                    param_list = [p.strip() for p in params.split(",") if p.strip()]

                    function_style = 'style="color: {}; font-weight: bold;"'.format(
                        self.color_schemes["calltip_function"]
                    )
                    param_style = 'style="color: {};"'.format(
                        self.color_schemes["calltip_param"]
                    )
                    description_style = 'style="color: {};"'.format(
                        self.color_schemes["calltip_description"]
                    )

                    formatted_params = []
                    for param in param_list:
                        if param.startswith("[") and param.endswith("]"):
                            formatted_params.append(
                                f'<span style="color: {self.color_schemes["calltip_optional_param"]};">{param}</span>'
                            )
                        else:
                            formatted_params.append(
                                f"<span {param_style}>{param}</span>"
                            )

                    params_str = ", ".join(formatted_params)

                    calltip = f"""
                    <div style="font-family: 'JetBrainsMono Nerd Font', monospace; font-size: 11px; padding: 5px;">
                        <span {function_style}>{function_name}</span>(<span>{params_str}</span>)
                        <br><br>
                        <span {description_style}>{description}</span>
                    </div>
                    """

                    self.codespace.callTip(
                        self.codespace.positionFromLineIndex(
                            *self.codespace.getCursorPosition()
                        ),
                        calltip,
                    )
                    logging.debug(f"Calltip shown: {word}")
                    return
            logging.debug(f"No calltip available for: {current_word}")
        except Exception as e:
            logging.exception(f"Error showing calltip: {e}")

    def get_lua_keywords(self) -> List[str]:
        return [
            # Keywords
            "and|Keyword: Logical AND operator",
            "break|Keyword: Exit from a loop",
            "do|Keyword: Start a block",
            "else|Keyword: Else in conditional statements",
            "elseif|Keyword: Else if in conditional statements",
            "end|Keyword: End a block",
            "false|Keyword: Boolean false value",
            "for|Keyword: Create a for loop",
            "function|Keyword: Define a function",
            "if|Keyword: Conditional statement",
            "in|Keyword: Part of the for loop syntax",
            "local|Keyword: Declare a local variable",
            "nil|Keyword: Represents a null value",
            "not|Keyword: Logical NOT operator",
            "or|Keyword: Logical OR operator",
            "repeat|Keyword: Start a repeat-until loop",
            "return|Keyword: Exit a function and return a value",
            "then|Keyword: Used in if statements",
            "true|Keyword: Boolean true value",
            "until|Keyword: End condition for repeat-until loop",
            "while|Keyword: Create a while loop",
            # Built-in Functions
            "assert(v [, message])|Function: Raises an error if the value of its argument v is false",
            "collectgarbage([opt [, arg]])|Function: Performs garbage collection",
            "dofile([filename])|Function: Opens the named file and executes its contents as a Lua chunk",
            "error(message [, level])|Function: Terminates the last protected function called and returns message as the error object",
            "getmetatable(object)|Function: Returns the metatable of the given object",
            "ipairs(t)|Function: Returns an iterator function, the table t, and 0",
            "load(chunk [, chunkname [, mode [, env]]])|Function: Loads a chunk",
            "loadfile([filename [, mode [, env]]])|Function: Loads a chunk from a file",
            "next(table [, index])|Function: Allows a program to traverse all fields of a table",
            "pairs(t)|Function: Returns the next function, the table t, and nil",
            "pcall(f [, arg1, ...])|Function: Calls function f with the given arguments in protected mode",
            "print(...)|Function: Receives any number of arguments and prints their values",
            "rawequal(v1, v2)|Function: Checks whether v1 is equal to v2, without invoking any metamethod",
            "rawget(table, index)|Function: Gets the real value of table[index], without invoking any metamethod",
            "rawlen(v)|Function: Returns the length of the object v, which must be a table or a string, without invoking any metamethod",
            "rawset(table, index, value)|Function: Sets the real value of table[index] to value, without invoking any metamethod",
            "select(index, ...)|Function: Returns all arguments after argument number index",
            "setmetatable(table, metatable)|Function: Sets the metatable for the given table",
            "tonumber(e [, base])|Function: Tries to convert its argument to a number",
            "tostring(v)|Function: Receives a value of any type and converts it to a string in a human-readable format",
            "type(v)|Function: Returns the type of its only argument, coded as a string",
            "xpcall(f, msgh [, arg1, ...])|Function: Similar to pcall, but sets a new message handler msgh",
            # String manipulation
            "string.byte(s [, i [, j]])|Function: Returns the internal numeric codes of the characters s[i], s[i+1], ..., s[j]",
            "string.char(...)|Function: Receives zero or more integers, converts each one to a character, and returns a string from all the results",
            "string.dump(function [, strip])|Function: Returns a string containing a binary representation of the given function",
            "string.find(s, pattern [, init [, plain]])|Function: Looks for the first match of pattern in the string s",
            "string.format(formatstring, ...)|Function: Returns a formatted version of its variable number of arguments following the description given in its first argument",
            "string.gmatch(s, pattern)|Function: Returns an iterator function that, each time it is called, returns the next captures from pattern over string s",
            "string.gsub(s, pattern, repl [, n])|Function: Returns a copy of s in which all (or the first n, if given) occurrences of the pattern have been replaced",
            "string.len(s)|Function: Returns the length of the string s",
            "string.lower(s)|Function: Returns a copy of the string with all uppercase letters changed to lowercase",
            "string.match(s, pattern [, init])|Function: Looks for the first match of pattern in the string s",
            "string.rep(s, n [, sep])|Function: Returns a string that is the concatenation of n copies of the string s",
            "string.reverse(s)|Function: Returns a string that is the string s reversed",
            "string.sub(s, i [, j])|Function: Returns the substring of s that starts at i and continues until j",
            "string.upper(s)|Function: Returns a copy of the string with all lowercase letters changed to uppercase",
            # Table manipulation
            "table.concat(list [, sep [, i [, j]]])|Function: Returns list[i]..sep..list[i+1]..sep..list[j]",
            "table.insert(list, [pos,] value)|Function: Inserts element value at position pos in list",
            "table.move(a1, f, e, t [,a2])|Function: Moves elements from table a1 to table a2",
            "table.pack(...)|Function: Returns a new table with all parameters stored into keys 1, 2, etc.",
            "table.remove(list [, pos])|Function: Removes from list the element at position pos",
            "table.sort(list [, comp])|Function: Sorts list elements in a given order, in-place",
            "table.unpack(list [, i [, j]])|Function: Returns the elements from the given list",
            # Mathematical functions
            "math.abs(x)|Function: Returns the absolute value of x",
            "math.acos(x)|Function: Returns the arc cosine of x (in radians)",
            "math.asin(x)|Function: Returns the arc sine of x (in radians)",
            "math.atan(y [, x])|Function: Returns the arc tangent of y/x (in radians)",
            "math.ceil(x)|Function: Returns the smallest integer larger than or equal to x",
            "math.cos(x)|Function: Returns the cosine of x (assumed to be in radians)",
            "math.deg(x)|Function: Returns the angle x (given in radians) in degrees",
            "math.exp(x)|Function: Returns the value e^x",
            "math.floor(x)|Function: Returns the largest integer smaller than or equal to x",
            "math.log(x [, base])|Function: Returns the logarithm of x in the given base",
            "math.max(x,...)|Function: Returns the maximum value among its arguments",
            "math.min(x,...)|Function: Returns the minimum value among its arguments",
            "math.pi|Constant: The value of π",
            "math.rad(x)|Function: Returns the angle x (given in degrees) in radians",
            "math.random([m [, n]])|Function: Returns a random number",
            "math.randomseed(x)|Function: Sets x as the seed for the pseudo-random generator",
            "math.sin(x)|Function: Returns the sine of x (assumed to be in radians)",
            "math.sqrt(x)|Function: Returns the square root of x",
            "math.tan(x)|Function: Returns the tangent of x (assumed to be in radians)",
        ]
