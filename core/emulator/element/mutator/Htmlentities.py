import html

from core.emulator.WAFElement import WAFElement


class Htmlentities(WAFElement):
    _encode_quotes = False

    def set_encode_quotes(self, flag: bool):
        self._encode_quotes = flag

    def process(self, payload: str):
        return html.escape(payload, self._encode_quotes)
