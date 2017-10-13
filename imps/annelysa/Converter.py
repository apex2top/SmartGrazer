import re


class Converter(object):
    @classmethod
    def getDecimal(cls, string):
        result = []
        for c in string:
            if type(c) is int:
                result.append(c)
            else:
                result.append(str(ord(c)))

        return result

    @classmethod
    def getString(cls, deciarray):
        result = ''

        for n in deciarray:
            if n.isdigit():
                n = int(n)
            result = result + chr(n)

        return result

    @classmethod
    def asciirepl(cls, match):
        # replace the hexadecimal characters with ascii characters
        s = match.group()

        return chr(int(s[-2:], 16))

    @classmethod
    def reformat_content(cls, data):
        p = re.compile(r'\\x(\w{2})')
        return p.sub(Converter.asciirepl, data)
