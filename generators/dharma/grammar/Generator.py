import os
import subprocess

from config.Configuration import Configuration


class Generator(object):
    """This class represents the context free tools generators from the open source project dharma.

        This software is using this generators in combination with the xss tools file "xss.dg".

        For more information visit: https://github.com/MozillaSecurity/dharma

    """
    config: None

    def __init__(self):
        self.config = Configuration()

    def generate(self, amount):
        """This function executes the dharma script with the predefined configuration.

        :return: List of generated payloads
        """
        script = os.path.realpath(os.getcwd() + self.config.get("dharma.script"))
        grammar = os.path.realpath(os.getcwd() + self.config.get("dharma.xss.tools"))

        if not os.path.isfile(script):
            print("E: Script [" + script + "] not found!")

        if not os.path.isfile(grammar):
            print("E: Grammar [" + grammar + "] not found!")

        # By setting the -logging option to 30, all dharma outputs where suppresed except the return values.
        command = self.config.get('python.path') + ' ' + script + " -grammars " + grammar + " -count " + str(
            amount) + " -logging 30"

        proc = subprocess.Popen(command, stdout=subprocess.PIPE)

        output = []
        for line in proc.stdout.readlines():

            if line == b'\r\n':
                continue

            output.append(line.replace(b'dharma', b'#smartgrazer'))

        return {'generator': self.__class__.__name__, 'payloads': output}
