import argparse
import logging


class Analyzer(object):
    payload = ""
    response = ""

    def __init__(self, payload, response):
        self.payload = payload
        self.response = response

    def run(self):
        if self.payload in self.response:
            logging.info("Payload was found in response!")
            return True
        else:
            print("Payload:\t" + str(self.payload))
            print("Response:\t" + str(self.response))
            return False


def main():
    parser = argparse.ArgumentParser(
        prog='Analyzer',
        usage='%(prog)s [options]',
        description='Compare the returned html response with the send payload.',
        formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-p',
                        '--payload',
                        required=True,
                        default='<script>alert(1)</script>',
                        help='The payload which was send.')

    parser.add_argument('-r',
                        '--response',
                        required=True,
                        nargs='+',
                        help="The websites' response.")

    params = parser.parse_args()

    analyzer = Analyzer(params.__dict__['payload'], params.__dict__['response'])


if __name__ == "__main__":
    main()
