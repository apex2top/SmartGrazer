from core.emulator.WAFElement import WAFElement


class WordFilter(WAFElement):
    _word = ''

    def __init__(self, word):
        self._word = word

    def process(self, payload: str):
        return payload.replace(self._word, "")
