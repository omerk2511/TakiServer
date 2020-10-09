from .message import Response


class TakiException(Exception):
    def __init__(self, status, message):
        super(TakiException, self).__init__()
        self.status = status
        self.message = message

    def response(self):
        return Response(self.status, message=self.message)
