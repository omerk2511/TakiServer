from message import Response
from codes import Codes

class Responses(object):
    # Hardcoded Responses
    GENERAL_SUCCESS = Response(Codes.SUCCESS).serialize()
    GENERAL_BAD_REQUEST = Response(Codes.BAD_REQUEST, message = 'Bad request').serialize()
