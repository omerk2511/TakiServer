from message import Response
from codes import Status


class Responses(object):
    # Hardcoded Responses
    SUCCESS = Response(Status.SUCCESS)
    BAD_REQUEST = Response(Status.BAD_REQUEST, message='Bad request')
    INTERNAL_ERROR = Response(Status.INTERNAL_ERROR,
                              message='Unknown internal error')
