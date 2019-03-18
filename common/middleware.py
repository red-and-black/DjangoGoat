
class CacheHeaderMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['Cache-Control'] = (
            'no-cache="Set-Cookie, Set-Cookie2", no-store, must-revalidate'
        )
        response['Pragma'] = 'no-cache'
        return response
