class Element(object):
    name = ''
    element = ''

    def __init__(self, name, element):
        self.name = name
        self.element = element

    def getName(self):
        return self.name

    def getRawElement(self):
        return self.element

    def getElement(self):
        if type(self.element) is str:
            return self.element

        return chr(self.element)
