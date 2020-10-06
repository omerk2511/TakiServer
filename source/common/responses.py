from message import Response
from codes import Codes, Statuses


class Responses(object):
    # Hardcoded Responses
    GENERAL_SUCCESS = Response(Statuses.SUCCESS)
    GENERAL_BAD_REQUEST = Response(Statuses.BAD_REQUEST, message = 'Bad request')
