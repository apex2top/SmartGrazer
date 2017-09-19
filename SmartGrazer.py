import argparse
import logging
from argparse import RawTextHelpFormatter

from Analyzer import Analyzer
from Executor import Executor
from Generator import Generator
from config.Configuration import Configuration
from generators.simple.Generator import Generator as SimpleGenerator


class SmartGrazer(object):
    """This class represents loads, configures and executes the softwares' compontents."""
    config = Configuration()

    #: The generators instance dynamically assigned depending on the configuration.
    generator = None

    def __init__(self, params):
        self.config.handle(params)

        logging.getLogger().setLevel(logging.INFO)
        logging.basicConfig(format='%(levelname)s:\t%(message)s')

    def run(self):
        # Create an instance of the configured Generator
        self.generator = (Generator(self.config.get('payload.generator'))).get()
        if self.generator is None:
            raise ValueError('Seems that no generator was found! Config: ' + self.config.get('payload.generator'))

        logging.info(">> SmartGrazer:\tGenerator \"" + self.config.get('payload.generator') + "\" loaded.")

        if self.config.get('payload.generator') == "dharma" and self.config.get('urlencode') == "True":
            print(
                "! SmartGrazer:\tDharma generates payloads with urlencoding. Enabling the --urlencode option, may cause double urlencoding on payloads! ")

        # Let the generator create some payloads...
        payloads = self.generator.generate(int(self.config.get('payload.generator.amount')))

        logging.info(">>\tGenerated " + self.config.get('payload.generator.amount') + " payloads.")

        # just print the results and exit
        if self.config.get('execute') is "False":
            for attempt in payloads['payloads']:
                print(attempt)
            exit(0)

        # basic check for parameter dependancies
        if self.config.get('target') == '' or self.config.get('valid.input') == '':
            print(
                "! SmartGrazer:\tYou enabled sending the payloads to a website. Please provide the -t and -vi parameters.")
            exit(1)

        # preparing the executor instance
        executor = Executor(self.config.get("target"), self.config.get("urlencode"))

        # testing the valid option first
        validresult = executor.send(
            self.config.get("valid.input").encode(),
            self.config.get('parameter.get'),
            self.config.get('parameter.post'),
            self.config.get('parameter.cookies')
        )

        success = (Analyzer(self.config.get("valid.input").encode(), validresult['response'])).run()

        simplegenerator = SimpleGenerator()

        randomString = simplegenerator.getRandomString().encode()
        randomStringTestResult = executor.send(
            randomString,
            self.config.get('parameter.get'),
            self.config.get('parameter.post'),
            self.config.get('parameter.cookies')
        )

        success = (Analyzer(randomString, randomStringTestResult['response'])).run()

        maxLengthString = simplegenerator.getMaxLengthRandomString().encode()
        maxLengthStringTestResult = executor.send(
            maxLengthString,
            self.config.get('parameter.get'),
            self.config.get('parameter.post'),
            self.config.get('parameter.cookies')
        )

        success = (Analyzer(maxLengthString, maxLengthStringTestResult['response'])).run()

        specialCharsString = simplegenerator.getSpecialChars().encode()
        specialCharsStringTestResult = executor.send(
            specialCharsString,
            self.config.get('parameter.get'),
            self.config.get('parameter.post'),
            self.config.get('parameter.cookies')
        )

        success = (Analyzer(specialCharsString, specialCharsStringTestResult['response'])).run()

        # Run the payloads against the website
        for attempt in payloads['payloads']:
            result = executor.send(
                attempt,
                self.config.get('parameter.get'),
                self.config.get('parameter.post'),
                self.config.get('parameter.cookies')
            )

            success = (Analyzer(attempt, result['response'])).run()


def main():
    """ This Function parses the command-line arguments and initiates the SmartGrazer software.

        General usage:

        :command: SmartGrazer [options]

        Full list of options available through:

        :command: SmartGrazer -h
    """

    parser = argparse.ArgumentParser(
        prog='SmartGrazer',
        usage='%(prog)s [options]',
        description='A smart tools based fuzzer.',
        formatter_class=RawTextHelpFormatter)

    parser.add_argument('-x',
                        '--execute',
                        default=False,
                        action='store_const',
                        const=True,
                        help='Wether to send the payload directly to the website or not.\nExecuting the ')

    parser.add_argument('-t',
                        '--target',
                        default=None,
                        help='URL to SUT (System Under Test).')

    parser.add_argument('-vi',
                        '--valid.input',
                        nargs='+',
                        help='Provide a valid input for the analyzer.'
                        )

    parser.add_argument('-pg',
                        '--parameter.get',
                        nargs='*',
                        help="A list of key-value arguments which will be send as 'GET' parameters.\nSet 'PAYLOAD' as value to send the generated attack.\nExample:\npython SmartGrazer.py ... -pg key1=value1 key2=value2 key3=PAYLOAD\n\n")

    parser.add_argument('-pp',
                        '--parameter.post',
                        nargs='*',
                        help="A list of key-value arguments which will be send as 'POST' parameters.\nSet 'PAYLOAD' as value to send the generated attack.\nExample:\npython SmartGrazer.py ... -pp key1=value1 key2=value2 key3=PAYLOAD\n\n")

    parser.add_argument('-pc',
                        '--parameter.cookies',
                        nargs='*',
                        help='A list of key-value arguments which will be send as "Cookies" parameters.')

    parser.add_argument('--urlencode',
                        default=False,
                        action='store_const',
                        const=True,
                        help='Reset the configuration to it\'s default values.')

    general_options = parser.add_argument_group("Smartgrazer options")
    general_options.add_argument('--reset',
                                 default=False,
                                 action='store_const',
                                 const=True,
                                 help='Reset the configuration to it\'s default values.')

    general_options.add_argument('--config',
                                 default=False,
                                 action='store_const',
                                 const=True,
                                 help='Show or edit the current configuration.')

    general_options.add_argument('-g',
                                 '--payload.generator.amount',
                                 nargs='?',
                                 type=int,
                                 help='How many payloads should be generated? Default: {0}'.format(
                                     5))
    general_options.add_argument('-G',
                                 '--payload.generator',
                                 choices=['smartgrazer', 'dharma'],
                                 help='Choose a payload generator. Default: \'smartgrazer\'')

    dharma_options = parser.add_argument_group("Dharma generator options")

    dharma_options.add_argument('-dp',
                                '--dharma.script',
                                help='Path to dharma script.')

    dharma_options.add_argument('-dg',
                                '--dharma.xss.tools',
                                help='Path to dharma xss tools definition file.')

    params = parser.parse_args()

    smartgrazer = SmartGrazer(params)
    smartgrazer.run()


if __name__ == "__main__":
    main()
