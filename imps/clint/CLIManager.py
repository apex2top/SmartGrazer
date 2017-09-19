import argparse
from argparse import RawTextHelpFormatter


class CLIManager(object):
    parser = None
    args = None

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog='SmartGrazer',
            usage='%(prog)s [options]',
            description='A smart tools based fuzzer.',
            formatter_class=RawTextHelpFormatter)
        pass

    def handle(self):
        self.parser.add_argument('-t',
                                 '--target',
                                 default='runconfig.default.json',
                                 help='Name of the configuration file containing the config.')

        self.parser.add_argument('--overwrite',
                                 nargs='*',
                                 help="A list of configuration params which should be overwritten temporarily.\nFor example:\n\t--overwrite imps.smithy.payload.amount=10 imps.smithy.generator=smarty")

        self.args = self.parser.parse_args()
        return self

    def getArgs(self):
        return self.args

    def get(self, key):
        if hasattr(self.args, key):
            return self.args.__dict__[key]

        return None

    def parseOverwrites(self):
        result = {}

        for pair in self.get("overwrite"):
            key, value = pair.split("=")

            steps = key.split(".")
            varname = steps[len(steps) - 1]

            cursor = result
            for step in steps:
                if step not in cursor:
                    if varname is step:
                        if value.isdigit():
                            value = int(value)
                        cursor[step] = value
                    else:
                        cursor[step] = {}
                cursor = cursor[step]
        return result
