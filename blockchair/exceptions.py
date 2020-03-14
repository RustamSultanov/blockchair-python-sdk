
class APIError(Exception):
    def __init__(self, message, code):
        Exception.__init__(self, message)
        self.code = code


class FormatError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)
