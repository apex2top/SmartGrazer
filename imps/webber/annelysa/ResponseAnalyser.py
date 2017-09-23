class ResponseAnalyser(object):
    response = ''
    runConfig = {}

    def __init__(self, config):
        self.config = config

    def loadResponse(self, file):
        f = open(file, 'r')
        self.response = f.read().encode("UTF-8")

    def loadRunConfig(self, file):
        renamed = file.replace(".html", '.json')
        f = open(renamed, 'r')
        config = f.read()

        self.runConfig = eval(config)

    def analyze(self):
        results = {
            "found": []
        }

        params = self.runConfig["action"]["params"]

        for type in params:
            for key in params[type]:
                value = params[type][key]
                if value.encode() in self.response:
                    results.append({key: "found"})
                else:
                    results.append({value: "not found"})

        return results
