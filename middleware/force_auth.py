from pyson.pylib import static, auth
# import view


class Force_auth:
    def __init__(self, application):
        self.application = application
        
    def __call__(self, environ, start_response):
        if not (environ['session'].has_key('auth') and environ['session']['auth']):
            if environ['PATH_INFO'].endswith('.css') | environ['PATH_INFO'].endswith('hedr33.png'):
                return static.StaticFile(environ, start_response)
            if (environ['PATH_INFO'].startswith('/login')) & (environ['REQUEST_METHOD'].upper() == 'POST'):
                return auth.authentification(environ, start_response)
                
                
            return auth.login(environ, start_response, environ['PATH_INFO'])
        return self.application(environ, start_response)
        
        
        

    
    
    
    
    
    
    
    