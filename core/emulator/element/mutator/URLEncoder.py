from urllib.parse import urlencode, quote_plus
from core.emulator.WAFElement import WAFElement


class URLEncoder(WAFElement):

    def process(self, payload: str):
        payload = {"payload" : payload}
        return urlencode(payload, quote_via=quote_plus).replace("payload=", "", 1)
