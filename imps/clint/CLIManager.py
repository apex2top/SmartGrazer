import argparse
from argparse import RawTextHelpFormatter


class CLIManager(object):
    """This class handles all cli inputs.
    """

    _parser = None
    _args = None

    def __init__(self):
        self._parser = argparse.ArgumentParser(
            prog='SmartGrazer',
            usage='%(prog)s [-h | [-g | -x path/to/runconfig.json] | --overwrite [key1=value1 ... keyn=valuen]]',
            description='A smart grammar based fuzzer.',
            formatter_class=RawTextHelpFormatter)

    def handle(self):
        """ This method creates the cli interface.

            :return: `CLIManager`
            :raises: ValueError -- If nor g or x -mode is selected.
        """
        mutual = self._parser.add_mutually_exclusive_group()

        mutual.add_argument('-g',
                            '--generate',
                            const=True,
                            nargs='?',
                            action='store',
                            default=False,
                            help='Just generate and output the payloads.')

        mutual.add_argument('-x',
                            '--execute',
                            help='Name of the configuration file containing the config.')

        self._parser.add_argument('--overwrite',
                                  nargs='*',
                                  default=[],
                                  help="A list of configuration params which should be overwritten temporarily.\nFor example:\n\t--overwrite smartgrazer.imps.smithy.generator=smarty smartgrazer.imps.smithy.generate.amount=5")

        self._parser.add_argument('-c',
                                 '--cleanup',
                                  const=True,
                                  nargs='?',
                                  default=False,
                                  action='store',
                                  help="Clean the previous stored responses.")

        self._parser.add_argument('--enableWebdriver',
                                  const=True,
                                  nargs='?',
                                  default=False,
                                  action='store',
                                  help="Enables live test for payload.\nThis Option requires either a gecko or a chrome webdriver binary in the subfolder:\nwebdriver/[YourOS]/")

        self._args = self._parser.parse_args()

        if self._args.execute == None and self._args.generate is False:
            raise ValueError("You either have to set the -g or the -x mode. Please see help with the -h option!")
            exit(1)

        return self

    def getArgs(self):
        return self._args

    def get(self, key):
        if hasattr(self._args, key):
            return self._args.__dict__[key]

        return []

    def parseOverwrites(self):
        """ This method takes the parameters from the --overwrite parameter and parses them,
            so they can be merged with the `imps.confy.JSONConfigManager` instance.

            :return: dict
        """
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
