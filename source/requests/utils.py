def validate_request(request):
    if 'code' in request and 'args' in request:
        return

    raise ValueError('Invalid request')
