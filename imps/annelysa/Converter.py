class Converter(object):
    @staticmethod
    def getDecimal(string):
        result = []
        for c in string:
            if type(c) is int:
                result.append(c)
            else:
                result.append(str(ord(c)))

        return result

    @staticmethod
    def getString(deciarray):
        result = ''

        for n in deciarray:
            if n.isdigit():
                n = int(n)
            result = result + chr(n)

        return result
