import argparse
import itertools
import urllib.request

from executor.Useragent import Useragent
from generators.smartgrazer.generator.encoder.Encoder import Encoder


class Executor(object):
    urlencode = False
    target = ''

    useragents = Useragent()
    encoder = Encoder()

    def __init__(self, target, urlencode=False):
        self.urlencode = urlencode
        self.target = target

    def send(self, payload, getParams, postParams=None, cookieParams=None):
        summary = {}

        query = getParams

        if "," in getParams:
            query = '&'.join(getParams.split(","))

        if self.urlencode is "True":
            getParamsList = query.split("=")

            for i in range(len(getParamsList)):
                getParamsList[i] = getParamsList[i].replace("PAYLOAD", payload.decode('utf-8'))

            paramsMap = dict(itertools.zip_longest(*[iter(getParamsList)] * 2, fillvalue=""))
            query = self.encoder.urlencode(paramsMap)
        else:
            query = query.replace("PAYLOAD", payload.decode('utf-8'))

        requeststring = '?'.join([self.target, query])

        if not postParams is "":
            print(postParams)
            if "," in postParams:
                query = '&'.join(postParams.split(","))

            getParamsList = query.split("=")

        else:
            postParams = None
        exit(0)
        print(requeststring)
        request = urllib.request.urlopen(requeststring, postParams)
        response = request.read()

        summary.update({'payload': payload, 'request': requeststring, 'response': response})

        return summary


def main():
    parser = argparse.ArgumentParser(
        prog='executor',
        usage='%(prog)s [options]',
        description='Simple payload executor',
        formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-t',
                        '--target',
                        required=True,
                        help='URL to SUT (System Under Test).')

    parser.add_argument('-p',
                        '--payload',
                        required=True,
                        default='<script>alert(1)</script>',
                        help='URL to SUT (System Under Test).')

    parser.add_argument('-pg',
                        '--parameter.get',
                        required=True,
                        nargs='+',
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

    params = parser.parse_args()

    executor = (Executor(params)).send()


if __name__ == "__main__":
    main()
