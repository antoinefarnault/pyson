"""restriction - permet de limiter des acces a des uri en fonction des roles

l'authentification des utilisateurs se fait dans la table user

"""
from pyson.pylib import framelib, auth
import role


class Middle:
    def __init__(self, application):
        self.application = application
        
        
    def __call__(self, environ, start_response):
        environ['permission'] = False
        for r in environ['session']['roles']:
            role.__dict__[r](environ, environ['PATH_INFO'])
            if environ['permission']:
                break
            
        if environ['permission']:
            return self.application(environ, start_response)
        
        if (not environ['session'].has_key('auth')) or (not environ['session']['auth']):
                return auth.login(environ, start_response, environ['PATH_INFO'])
        return framelib.send_404(start_response, "Vous n'avez pas les droits sur cette page ")
   
   
   
