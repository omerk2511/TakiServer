class Responses(object):
    # Hardcoded Responses
    GENERAL_SUCCESS = {
        'status': 'success',
        'args': {}
    }

    GENERAL_BAD_REQUEST = {
        'status': 'bad_request',
        'args': {
            'message': 'Bad request'
        }
    }
