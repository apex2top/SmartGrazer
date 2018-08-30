from core.emulator import WAFElement
from core.entities import Payload


class WAF(object):
    _elements = []

    def __add__(self, element: WAFElement):
        self._elements.append(element)

    def test(self, payload: Payload):
        for element in self._elements:
            if not str(payload) == element.process(str(payload)):
                return False

        return True