import os
import subprocess

from imps.smithy.GeneratorGeneral import GeneratorGeneral
from imps.smithy.smarty.grammar.attacks.Attack import Attack


class PayloadGenerator(GeneratorGeneral):
    """This class represents the context free tools generators from the open source project dharma.

        This software is using this generator in combination with the xss tools file "smartgrazer.dg".

        The "smartgrazer.dg" file produces xss payloads in a comma separated way, so that this application can parse them.
        The "xss.dg" file from dharma generates non separated payloads.

        For more information visit: https://github.com/MozillaSecurity/dharma

    """
    _script = 'dharma.py'
    _grammar = 'xss.dg'

    def applyConfig(self, configuration):
        self._script = os.getcwd() + configuration["script"]
        self._grammar = os.getcwd() + configuration["grammar"]

        if not os.path.isfile(self._script):
            raise ValueError("Dharma file was not found! Given path: " + self._script)

        if not os.path.isfile(self._grammar):
            raise ValueError("Dharma file was not found! Given path: " + self._grammar)

    def generate(self, amount):
        """ This function executes the dharma script with the predefined configuration.

            :param: amount: int - The amount of requested payloads.
            :return: list<str> --the generated payloads
        """

        # By setting the -logging option to 30, all dharma outputs where suppresed except the return values.
        command = 'python ' + self._script + " -grammars " + self._grammar + " -count " + str(
            amount) + " -logging 30"

        proc = subprocess.Popen(command, stdout=subprocess.PIPE)

        output = []
        for line in proc.stdout.readlines():

            if line == b'\r\n':
                continue

            line = line.decode("utf-8")
            line = str(line)

            elements = self._parse(line[1:-3])
            attack = Attack(elements)
            output.append(attack)

        return output

    def _parse(self, payload):
        """
            This method parses the generated dharma strings into SmartGrazer elements.

            :param payload: str - The generated output from dharma.

            :return: list<`imps.smithy.elements.Element.Element`> -- The parsed elements.
        """
        list = payload.split(",")

        elements = []
        for entry in list:
            element = self.getElements().getElement(entry)
            elements.append(element)

        return elements
