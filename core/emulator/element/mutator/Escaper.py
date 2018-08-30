from core.emulator.WAFElement import WAFElement


class Escaper(WAFElement):

    _char: str
    _escape_char: str

    def __init__(self, char = "", escape_char = "\\"):
        self._char = char
        self._escape_char = escape_char

    def process(self, payload: str):
        return payload.replace(self._char, self._escape_char)