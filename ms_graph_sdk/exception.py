class TeamsApiException(Exception):

    def __init__(self, code, message):
        super().__init__(code+' '+message)
