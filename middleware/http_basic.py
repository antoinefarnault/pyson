""" http_basic - Module d'authentification par le protocol http basic
"""
import base64, string
from pyson.pylib import auth

class Http_basic:
    def __init__(self, application):
        self.application = application
        
        
    
    def __call__(self, environ, start_response):
        authorization = environ.get('HTTP_AUTHORIZATION')
        if authorization:
#             print '#v http_basic autentification'
            (username, password) = string.split(base64.decodestring(string.split((authorization), ' ')[1]), ':')
            if auth.login(environ, username, password):
                return self.application(environ, start_response)
#         print "#v demande d'authentification http_basic"
        start_response("401 Unauthorised", [('WWW-Authenticate', 'Basic realm="eh oui"')])
        return ["Unauthorised"]        