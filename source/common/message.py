import json

class Request(object):
    def __init__(self, code, args):
        self.code = code
        self.args = args


    @classmethod
    def deserialize(cls, data):
        if 'code' not in data or 'args' not in data:
            raise Exception('Invalid message')

        return cls(data['code'], data['args'])





class Response(object):
    def __init__(self, status, args):
        self.status = status
        self.args = args


    def serialize(self):
        return json.dumps(
            {
                "status": self.status,
                "args": self.args
            }
        )




class Message(object): 
    def __init__(self, code, args):
        self.code = code
        self.args = args


    def serialize(self):
        return json.dumps(
            {
                "status": self.code,
                "args": self.args
            }
        )
    
    @classmethod
    def deserialize(cls, data):
        message = data

        if 'code' not in message or 'args' not in message:
            raise Exception('Invalid message')

        return cls(message['code'], message['args'])

