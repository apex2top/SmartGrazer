import os
import subprocess


class PayloadGenerator(object):
    """This class represents the context free tools generators from the open source project dharma.

        This software is using this generators in combination with the xss tools file "xss.dg".

        For more information visit: https://github.com/MozillaSecurity/dharma

    """
    _script = 'dharma.py'
    _grammar = 'xss.dg'

    def applyConfig(self, configuration):
        self._script = os.path.realpath(os.getcwd() + configuration["script"])
        self._grammar = os.path.realpath(os.getcwd() + configuration["grammar"])

        if not os.path.isfile(self._script):
            raise ValueError("Dharma file was not found! Given path: " + self._script)

        if not os.path.isfile(self._grammar):
            raise ValueError("Dharma file was not found! Given path: " + self._grammar)

    def generate(self, amount):
        """This function executes the dharma script with the predefined configuration.

        :return: the generated payloads
        """

        # By setting the -logging option to 30, all dharma outputs where suppresed except the return values.
        command = 'python ' + self._script + " -grammars " + self._grammar + " -count " + str(
            amount) + " -logging 30"

        proc = subprocess.Popen(command, stdout=subprocess.PIPE)

        output = []
        for line in proc.stdout.readlines():

            if line == b'\r\n':
                continue

            line = line.replace(b'dharma', b'#smartgrazer')
            line = line.decode("utf-8")
            line = str(line)

            output.append(line)

        return output
