class Converter(object):
    """This Class contains conversion methods for converting decimal arrays into string and vica versa."""

    @classmethod
    def getDecimal(cls, input):
        """ This method converts a string into a corresponding array of decimals

            :param input: The input string to convert.
            :type input: str.

            :returns:  list<int> -- the converted string.
        """
        result = []
        for c in input:
            if type(c) is int:
                result.append(c)
            else:
                result.append(str(ord(c)))

        return result

    @classmethod
    def getString(cls, deciarray):
        """ This method converts a string into a corresponding array of decimals

            :param deciarray: The input array to convert.
            :type deciarray: list<int>.

            :returns:  list<int> -- the converted string.
        """
        result = ''

        for n in deciarray:
            if n.isdigit():
                n = int(n)
            result = result + chr(n)

        return result
