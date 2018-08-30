import re

from core.emulator.WAFElement import WAFElement


class TagFilter(WAFElement):
    _tag = ''

    def __init__(self, tag: str):
        self._tag = tag

    def process(self, payload: str):
        return re.sub("<(/)?" + self._tag + ">", "", payload)
