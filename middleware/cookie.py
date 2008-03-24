""" cookie - Middleware de gestion de cookie
"""


class Cookie:
    def __init__(self, application):
        self._application = application
   
   
    def __call__(self, environ, start_response):
        
        def start_response_wrapper(status, response_headers, exc_info=None):
            
            if environ.has_key('set_cookie'):
                response_headers.extend(environ['set_cookie'])
            start_response(status, response_headers, exc_info)
            
        return self._application(environ, start_response_wrapper)
