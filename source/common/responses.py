from message import Response
from codes import Code, Status


class Responses(object):
    # Hardcoded Responses
    GENERAL_SUCCESS = Response(Status.SUCCESS)
    GENERAL_BAD_REQUEST = Response(Status.BAD_REQUEST, message = 'Bad request')
