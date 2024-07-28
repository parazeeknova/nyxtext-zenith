import logging

import jedi  # type: ignore
from PyQt6.Qsci import QsciAPIs, QsciLexerPython, QsciScintilla
from PyQt6.QtCore import QMetaObject, QObject, Qt, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QColor, QFont

logging.basicConfig(
    level=logging.DEBUG,
    filename="zenith_debug.log",
    filemode="w",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


class PythonFeatures(QObject):
    updateRequired = pyqtSignal()

    def __init__(self, codespace, color_schemes):
        super().__init__(codespace)
        self.codespace = codespace
        self.color_schemes = color_schemes
        self.api = None
        QMetaObject.invokeMethod(self, "initialize", Qt.ConnectionType.QueuedConnection)

    @pyqtSlot()
    def initialize(self):
        try:
            self.customize_lexer()
            self.api = QsciAPIs(self.codespace.lexer())
            self.setup_autocompletion()
            self.setup_calltips()
            logging.info("PythonFeatures initialized successfully")
        except Exception as e:
            logging.exception(f"Error initializing PythonFeatures: {e}")

    def customize_lexer(self):
        try:
            lexer = QsciLexerPython(self.codespace)
            self.codespace.setLexer(lexer)

            default_font = QFont("JetBrainsMono Nerd Font", 10)
            lexer.setFont(default_font)

            comment_font = QFont("JetBrainsMono Nerd Font", 10, italic=True)
            lexer.setFont(comment_font, QsciLexerPython.Comment)

            keyword_font = QFont(
                "JetBrainsMono Nerd Font", 10, weight=QFont.Weight.Bold
            )
            lexer.setFont(keyword_font, QsciLexerPython.Keyword)

            number_font = QFont("JetBrainsMono Nerd Font", 10, weight=QFont.Weight.Bold)
            lexer.setFont(number_font, QsciLexerPython.Number)

            for style, color_key in [
                (QsciLexerPython.Default, "default"),
                (QsciLexerPython.Keyword, "keyword"),
                (QsciLexerPython.Number, "numbers"),
                (QsciLexerPython.DoubleQuotedString, "string"),
                (QsciLexerPython.SingleQuotedString, "string2"),
                (QsciLexerPython.TripleSingleQuotedString, "string"),
                (QsciLexerPython.TripleDoubleQuotedString, "string2"),
                (QsciLexerPython.Comment, "comment"),
                (QsciLexerPython.CommentBlock, "comment"),
                (QsciLexerPython.Identifier, "default"),
                (QsciLexerPython.Operator, "operators"),
                (QsciLexerPython.FunctionMethodName, "func"),
                (QsciLexerPython.ClassName, "class"),
                (QsciLexerPython.Decorator, "keyword"),
            ]:
                lexer.setColor(QColor(self.color_schemes[color_key]), style)

            # Explicitly set margin colors
            self.codespace.setMarginsForegroundColor(
                QColor(self.color_schemes["margin_fg"])
            )
            self.codespace.setMarginsBackgroundColor(
                QColor(self.color_schemes["margin_bg"])
            )

            logging.info("Python lexer customized successfully")
        except Exception as e:
            logging.exception(f"Error customizing Python lexer: {e}")

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

            for keyword in self.get_python_keywords():
                word, description = keyword.split("|")
                self.api.add(f"{word} - {description}")

            self.api.prepare()
            self.codespace.textChanged.connect(self.update_autocompletion)
            logging.info("Autocompletion set up successfully")
        except Exception as e:
            logging.exception(f"Error setting up autocompletion: {e}")

            self.api.prepare()
            self.codespace.textChanged.connect(self.update_autocompletion)
            logging.info("Autocompletion set up successfully")
        except Exception as e:
            logging.exception(f"Error setting up autocompletion: {e}")

    def setup_calltips(self):
        try:
            self.codespace.setCallTipsStyle(QsciScintilla.CallTipsStyle.CallTipsContext)
            self.codespace.setCallTipsVisible(0)
            self.codespace.callTipsStyle()
            self.codespace.cursorPositionChanged.connect(self.show_calltip)
            logging.info("Calltips set up successfully")
        except Exception as e:
            logging.exception(f"Error setting up calltips: {e}")

    def update_autocompletion(self):
        try:
            script = jedi.Script(
                code=self.codespace.text(), path=self.codespace.file_path
            )
            completions = script.complete(
                line=self.codespace.getCursorPosition()[0] + 1,
                column=self.codespace.getCursorPosition()[1],
            )

            self.api.clear()
            for completion in completions:
                description = (
                    completion.description
                    if completion.description
                    else completion.type
                )
                self.api.add(f"{completion.name} - {description}")

            # Add keyword completions
            for keyword in self.get_python_keywords():
                word, description = keyword.split("|")
                self.api.add(f"{word} - {description}")

            # Add type-specific method completions
            current_word = self.get_current_word()
            if current_word:
                type_methods = {
                    "list": [
                        kw
                        for kw in self.get_python_keywords()
                        if kw.startswith("list.")
                    ],
                    "str": [
                        kw for kw in self.get_python_keywords() if kw.startswith("str.")
                    ],
                    "dict": [
                        kw
                        for kw in self.get_python_keywords()
                        if kw.startswith("dict.")
                    ],
                    "tuple": [
                        kw
                        for kw in self.get_python_keywords()
                        if kw.startswith("tuple.")
                    ],
                    "set": [
                        kw for kw in self.get_python_keywords() if kw.startswith("set.")
                    ],
                }

                for type_name, methods in type_methods.items():
                    if current_word.endswith(f"{type_name}."):
                        for method in methods:
                            word, description = method.split("|")
                            self.api.add(f"{word[len(type_name)+1:]} - {description}")

            self.api.prepare()
            self.updateRequired.emit()
            logging.debug(f"Autocompletion updated with {len(completions)} completions")
        except Exception as e:
            logging.exception(f"Error updating autocompletion: {e}")

    def show_calltip(self):
        try:
            script = jedi.Script(
                code=self.codespace.text(), path=self.codespace.file_path
            )
            signatures = script.get_signatures(
                line=self.codespace.getCursorPosition()[0] + 1,
                column=self.codespace.getCursorPosition()[1],
            )

            if signatures:
                signature = signatures[0]
                params = ", ".join(param.name for param in signature.params)
                description = next(
                    (
                        kw.split("|")[1]
                        for kw in self.get_python_keywords()
                        if kw.startswith(f"{signature.name}|")
                    ),
                    "",
                )
                calltip = f"{signature.name}({params})\n{description}"
                self.codespace.callTip(
                    self.codespace.positionFromLineIndex(
                        *self.codespace.getCursorPosition()
                    ),
                    calltip,
                )
                logging.debug(f"Calltip shown: {calltip}")
            else:
                logging.debug("No calltip available at current position")
        except Exception as e:
            logging.exception(f"Error showing calltip: {e}")

    def get_current_word(self):
        line, index = self.codespace.getCursorPosition()
        text = self.codespace.text(line)
        word_end = index
        while (
            word_end < len(text) and text[word_end].isalnum() or text[word_end] in "_."
        ):
            word_end += 1
        word_start = index
        while (
            word_start > 0
            and text[word_start - 1].isalnum()
            or text[word_start - 1] in "_."
        ):
            word_start -= 1
        return text[word_start:word_end]

    def get_python_keywords(self):
        return [
            # Keywords
            "False|Keyword: Boolean false value",
            "None|Keyword: Null object or singleton",
            "True|Keyword: Boolean true value",
            "and|Keyword: Logical AND operator",
            "as|Keyword: Part of the import statement",
            "assert|Keyword: Debugging aid for checking conditions",
            "async|Keyword: Declare an asynchronous function or context manager",
            "await|Keyword: Used to call an asynchronous function",
            "break|Keyword: Exit from a loop",
            "class|Keyword: Define a class",
            "continue|Keyword: Continue to the next iteration of a loop",
            "def|Keyword: Define a function",
            "del|Keyword: Delete a reference to an object",
            "elif|Keyword: Else if in conditional statements",
            "else|Keyword: Else in conditional statements",
            "except|Keyword: Used in try/except blocks for exception handling",
            "finally|Keyword: Used in try/except blocks, always executed",
            "for|Keyword: Create a for loop",
            "from|Keyword: Part of the import statement",
            "global|Keyword: Declare a global variable",
            "if|Keyword: Conditional statement",
            "import|Keyword: Import a module",
            "in|Keyword: Membership test operator",
            "is|Keyword: Identity operator",
            "lambda|Keyword: Create an anonymous function",
            "nonlocal|Keyword: Declare a non-local variable",
            "not|Keyword: Logical NOT operator",
            "or|Keyword: Logical OR operator",
            "pass|Keyword: Null statement, does nothing",
            "raise|Keyword: Raise an exception",
            "return|Keyword: Exit a function and return a value",
            "try|Keyword: Start a try/except block",
            "while|Keyword: Create a while loop",
            "with|Keyword: Context manager",
            "yield|Keyword: Define a generator function",
            "yield from|Keyword: Delegate to a subgenerator",
            # Built-in Functions
            "abs(x)|Function: Return the absolute value of a number",
            "all(iterable)|Function: Return True if all elements of the iterable are true",
            "any(iterable)|Function: Return True if any element of the iterable is true",
            "ascii(object)|Function: Return a string containing a printable representation of an object",
            "bin(x)|Function: Convert an integer to a binary string",
            "bool([x])|Function: Convert a value to Boolean",
            "breakpoint(*args, **kws)|Function: Drops you into the debugger at the call site",
            "bytearray([source[, encoding[, errors]]])|Function: Return a new array of bytes",
            "bytes([source[, encoding[, errors]]])|Function: Return a new 'bytes' object",
            "callable(object)|Function: Return True if the object appears callable",
            "chr(i)|Function: Return a string of one character whose Unicode code point is the integer i",
            "classmethod(function)|Function: Transform a method into a class method",
            "compile(source, filename, mode, flags=0, dont_inherit=False, optimize=-1)|Function: Compile source into a code or AST object",
            "complex([real[, imag]])|Function: Create a complex number",
            "delattr(object, name)|Function: Delete a named attribute from an object",
            "dict(**kwarg)|Function: Create a new dictionary",
            "dir([object])|Function: Return list of names in the current local scope or attributes of object",
            "divmod(a, b)|Function: Return a pair of numbers consisting of quotient and remainder",
            "enumerate(iterable, start=0)|Function: Return an enumerate object",
            "eval(expression[, globals[, locals]])|Function: Evaluate a Python expression",
            "exec(object[, globals[, locals]])|Function: Execute Python code dynamically",
            "filter(function, iterable)|Function: Construct an iterator from elements which are true",
            "float([x])|Function: Convert a string or number to a floating point number",
            "format(value[, format_spec])|Function: Convert a value to a formatted representation",
            "frozenset([iterable])|Function: Return a new frozenset object",
            "getattr(object, name[, default])|Function: Get a named attribute from an object",
            "globals()|Function: Return the current global symbol table as a dictionary",
            "hasattr(object, name)|Function: Return True if the object has the given named attribute",
            "hash(object)|Function: Return the hash value of an object",
            "help([object])|Function: Invoke the built-in help system",
            "hex(x)|Function: Convert an integer to a hexadecimal string",
            "id(object)|Function: Return the identity of an object",
            "input([prompt])|Function: Read a string from standard input",
            "int([x[, base=10]])|Function: Convert a number or string to an integer",
            "isinstance(object, classinfo)|Function: Return True if the object is an instance of a class",
            "issubclass(class, classinfo)|Function: Return True if a class is a subclass of another class",
            "iter(object[, sentinel])|Function: Return an iterator object",
            "len(s)|Function: Return the length (number of items) of an object",
            "list([iterable])|Function: Create a list",
            "locals()|Function: Return the current local symbol table as a dictionary",
            "map(function, iterable, ...)|Function: Apply function to every item of iterable and return a list",
            "max(iterable, *[, key, default])|Function: Return the largest item in an iterable",
            "memoryview(obj)|Function: Create a memory view object",
            "min(iterable, *[, key, default])|Function: Return the smallest item in an iterable",
            "next(iterator[, default])|Function: Retrieve the next item from the iterator",
            "object()|Function: Return a new featureless object",
            "oct(x)|Function: Convert an integer to an octal string",
            "open(file, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None)|Function: Open file and return a file object",
            "ord(c)|Function: Return an integer representing the Unicode code point of a character",
            "pow(base, exp[, mod])|Function: Return base to the power exp; if mod is present, return base to the power exp, modulo mod",
            "print(*objects, sep=' ', end='\\n', file=sys.stdout, flush=False)|Function: Print objects to the text stream file",
            "property(fget=None, fset=None, fdel=None, doc=None)|Function: Return a property attribute",
            "range(stop)|Function: Return an immutable sequence type",
            "repr(object)|Function: Return a string containing a printable representation of an object",
            "reversed(seq)|Function: Return a reverse iterator",
            "round(number[, ndigits])|Function: Round a number to a given precision in decimal digits",
            "set([iterable])|Function: Return a new set object",
            "setattr(object, name, value)|Function: Set a named attribute on an object",
            "slice(stop)|Function: Create a slice object",
            "sorted(iterable, *, key=None, reverse=False)|Function: Return a new sorted list from the items in iterable",
            "staticmethod(function)|Function: Transform a method into a static method",
            "str(object='')|Function: Return a string version of an object",
            "sum(iterable, /, start=0)|Function: Sum of items in an iterable",
            "super([type[, object-or-type]])|Function: Return a proxy object that delegates method calls",
            "tuple([iterable])|Function: Create a tuple",
            "type(object)|Function: Return the type of an object",
            "vars([object])|Function: Return the __dict__ attribute for a module, class, instance, or any object",
            "zip(*iterables)|Function: Create an iterator of tuples",
            "__import__(name, globals=None, locals=None, fromlist=(), level=0)|Function: Import a module",
            # List operations
            "list.append(x)|Method: Add an item to the end of the list",
            "list.extend(iterable)|Method: Extend the list by appending all the items from the iterable",
            "list.insert(i, x)|Method: Insert an item at a given position",
            "list.remove(x)|Method: Remove the first item from the list whose value is equal to x",
            "list.pop([i])|Method: Remove the item at the given position in the list, and return it",
            "list.clear()|Method: Remove all items from the list",
            "list.index(x[, start[, end]])|Method: Return zero-based index in the list of the first item whose value is equal to x",
            "list.count(x)|Method: Return the number of times x appears in the list",
            "list.sort(*, key=None, reverse=False)|Method: Sort the items of the list in place",
            "list.reverse()|Method: Reverse the elements of the list in place",
            "list.copy()|Method: Return a shallow copy of the list",
            # String operations
            "str.capitalize()|Method: Return a capitalized version of the string",
            "str.casefold()|Method: Return a casefolded copy of the string",
            "str.center(width[, fillchar])|Method: Return centered in a string of length width",
            "str.count(sub[, start[, end]])|Method: Return the number of non-overlapping occurrences of substring sub",
            "str.encode(encoding='utf-8', errors='strict')|Method: Return an encoded version of the string as a bytes object",
            "str.endswith(suffix[, start[, end]])|Method: Return True if the string ends with the specified suffix",
            "str.expandtabs(tabsize=8)|Method: Return a copy of the string where all tab characters are replaced by one or more spaces",
            "str.find(sub[, start[, end]])|Method: Return the lowest index in the string where substring sub is found",
            "str.format(*args, **kwargs)|Method: Perform a string formatting operation",
            "str.index(sub[, start[, end]])|Method: Like find(), but raise ValueError when the substring is not found",
            "str.isalnum()|Method: Return True if all characters in the string are alphanumeric",
            "str.isalpha()|Method: Return True if all characters in the string are alphabetic",
            "str.isascii()|Method: Return True if all characters in the string are ASCII",
            "str.isdecimal()|Method: Return True if all characters in the string are decimal characters",
            "str.isdigit()|Method: Return True if all characters in the string are digits",
            "str.islower()|Method: Return True if all cased characters in the string are lowercase",
            "str.isnumeric()|Method: Return True if all characters in the string are numeric characters",
            "str.isprintable()|Method: Return True if all characters in the string are printable",
            "str.isspace()|Method: Return True if all characters in the string are whitespace",
            "str.istitle()|Method: Return True if the string is a titlecased string",
            "str.isupper()|Method: Return True if all cased characters in the string are uppercase",
            "str.join(iterable)|Method: Return a string which is the concatenation of the strings in iterable",
            "str.ljust(width[, fillchar])|Method: Return the string left justified in a string of length width",
            "str.lower()|Method: Return a copy of the string converted to lowercase",
            "str.lstrip([chars])|Method: Return a copy of the string with leading characters removed",
            "str.partition(sep)|Method: Split the string at the first occurrence of sep",
            "str.replace(old, new[, count])|Method: Return a copy of the string with all occurrences of substring old replaced by new",
            "str.rfind(sub[, start[, end]])|Method: Return the highest index in the string where substring sub is found",
            "str.rindex(sub[, start[, end]])|Method: Like rfind() but raises ValueError when the substring is not found",
            "str.rjust(width[, fillchar])|Method: Return the string right justified in a string of length width",
            "str.rpartition(sep)|Method: Split the string at the last occurrence of sep",
            "str.rsplit(sep=None, maxsplit=-1)|Method: Return a list of the words in the string, using sep as the delimiter string",
            "str.rstrip([chars])|Method: Return a copy of the string with trailing characters removed",
            "str.split(sep=None, maxsplit=-1)|Method: Return a list of the words in the string, using sep as the delimiter string",
            "str.splitlines([keepends])|Method: Return a list of the lines in the string, breaking at line boundaries",
            "str.startswith(prefix[, start[, end]])|Method: Return True if string starts with the specified prefix",
            "str.strip([chars])|Method: Return a copy of the string with leading and trailing characters removed",
            "str.swapcase()|Method: Return a copy of the string with uppercase characters converted to lowercase and vice versa",
            "str.title()|Method: Return a titlecased version of the string",
            "str.translate(table)|Method: Return a copy of the string in which each character has been mapped through the given translation table",
            "str.upper()|Method: Return a copy of the string converted to uppercase",
            "str.zfill(width)|Method: Return the numeric string left filled with zeros in a string of length width",
            # Dictionary operations
            "dict.clear()|Method: Remove all items from the dictionary",
            "dict.copy()|Method: Return a shallow copy of the dictionary",
            "dict.fromkeys(seq[, value])|Method: Create a new dictionary with keys from seq and values set to value",
            "dict.get(key[, default])|Method: Return the value for key if key is in the dictionary, else default",
            "dict.items()|Method: Return a new view of the dictionary's items ((key, value) pairs)",
            "dict.keys()|Method: Return a new view of the dictionary's keys",
            "dict.pop(key[, default])|Method: Remove specified key and return the corresponding value",
            "dict.popitem()|Method: Remove and return a (key, value) pair from the dictionary",
            "dict.setdefault(key[, default])|Method: Insert key with a value of default if key is not in the dictionary",
            "dict.update([other])|Method: Update the dictionary with the key/value pairs from other, overwriting existing keys",
            "dict.values()|Method: Return a new view of the dictionary's values",
            # Tuple operations
            "tuple.count(x)|Method: Return number of occurrences of value x in the tuple",
            "tuple.index(x[, start[, end]])|Method: Return index of first occurrence of value x in the tuple",
            # Set operations
            "set.add(elem)|Method: Add element elem to the set",
            "set.clear()|Method: Remove all elements from the set",
            "set.copy()|Method: Return a shallow copy of the set",
            "set.difference(*others)|Method: Return the difference of two or more sets as a new set",
            "set.difference_update(*others)|Method: Remove all elements of another set from this set",
            "set.discard(elem)|Method: Remove an element from a set if it is a member",
            "set.intersection(*others)|Method: Return the intersection of two or more sets as a new set",
            "set.intersection_update(*others)|Method: Update the set with the intersection of itself and another",
            "set.isdisjoint(other)|Method: Return True if two sets have a null intersection",
            "set.issubset(other)|Method: Test whether every element in the set is in other",
            "set.issuperset(other)|Method: Test whether every element in other is in the set",
            "set.pop()|Method: Remove and return an arbitrary element from the set",
            "set.remove(elem)|Method: Remove element elem from the set",
            "set.symmetric_difference(other)|Method: Return the symmetric difference of two sets as a new set",
            "set.symmetric_difference_update(other)|Method: Update a set with the symmetric difference of itself and another",
            "set.union(*others)|Method: Return the union of sets as a new set",
            "set.update(*others)|Method: Update the set, adding elements from all others",
        ]
