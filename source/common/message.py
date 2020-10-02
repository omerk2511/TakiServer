import json

class Request(object):
    def __init__(self, code, **kwargs): # each request has code and args
        self.code = code
        self.args = kwargs

    @classmethod
    def deserialize(cls, request):
        if 'code' not in request or 'args' not in request:
            raise Exception('Invalid message')

        return cls(request['code'], **request['args'])
 

class Response(object):
    def __init__(self, status, **kwargs): # each response has status and args. 
        self.status = status
        self.args = kwargs

    def serialize(self):
        return json.dumps(
            {
                'status': self.status,
                'args': self.args
            }
        )
