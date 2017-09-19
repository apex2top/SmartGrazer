import imps.confy.JSONConfigManager.JSONConfigManager as Confy


class RequestExecutor(object):
    confy = None

    def __init__(self):
        self.confy = Confy()
        pass
