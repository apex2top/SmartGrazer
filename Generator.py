import argparse

from generators.dharma.grammar.Generator import Generator as DharmaGenerator
from generators.smartgrazer.Generator import Generator as SmartGrazerGenerator


class Generator(object):
    generator = None

    type_dharma = "dharma"
    type_smartgrazer = "smartgrazer"

    def __init__(self, type):
        if type == self.type_dharma:
            self.generator = DharmaGenerator()
        elif type == self.type_smartgrazer:
            self.generator = SmartGrazerGenerator()

    def get(self):
        return self.generator

    def generate(self, amount):
        return self.generator.generate(amount)


def main():
    parser = argparse.ArgumentParser(
        prog='GraBaGen',
        usage='%(prog)s [options]',
        description='Grammar Based Generator',
        formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-g',
                        '--payload.generator.amount',
                        nargs='?',
                        default=5,
                        type=int,
                        help='How many payloads should be generated? Default: {0}'.format(
                            5))
    parser.add_argument('-G',
                        '--payload.generator',
                        default='smartgrazer',
                        choices=['smartgrazer', 'dharma'],
                        help='Choose a payload generators. Default: \'smartgrazer\'')

    params = parser.parse_args()

    print(params)

    print((Generator(params.__dict__['payload.generator'])).generate(params.__dict__['payload.generator.amount']))


if __name__ == "__main__":
    main()
