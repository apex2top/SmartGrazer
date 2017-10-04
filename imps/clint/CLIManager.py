import argparse
from argparse import RawTextHelpFormatter


class CLIManager(object):
    parser = None
    args = None

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog='SmartGrazer',
            usage='%(prog)s [-h | [-g | -x path/to/runconfig.json] | --overwrite [key1=value1 ... keyn=valuen]]',
            description='A smart tools based fuzzer.',
            formatter_class=RawTextHelpFormatter)
        pass

    def handle(self):

        mutual = self.parser.add_mutually_exclusive_group()

        mutual.add_argument('-g',
                            '--generate',
                            const=True,
                            nargs='?',
                            action='store',
                            default=False,
                            help='Name of the configuration file containing the config.')

        mutual.add_argument('-x',
                            '--execute',
                            help='Name of the configuration file containing the config.')

        self.parser.add_argument('--overwrite',
                                 nargs='*',
                                 default=[],
                                 help="A list of configuration params which should be overwritten temporarily.\nFor example:\n\t--overwrite imps.smithy.payload.amount=10 imps.smithy.generator=smarty")

        self.args = self.parser.parse_args()

        if self.args.execute == None and self.args.generate is False:
            raise ValueError("You either have to set the -g or the -x mode. Please see help with the -h option!")
            exit(1)

        return self

    def getArgs(self):
        return self.args

    def get(self, key):
        if hasattr(self.args, key):
            return self.args.__dict__[key]

        return []

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
