"""Middleware de gestion de session

Gestion des sessions par l'intermedaire de cookies.
Ces sessions sont persistante et stockee sur disque par
l'intermediaire du module pickle dans le dossier /tmp

Un cookie de session est de la forme SID = a_160_bits_key
Apres la mise en place d'une session le dictionnaire environ['session'] 
est disponible. Par default il ne contient que la cle 'id' accessible par
environ['session']['id']
Il est possible de rajouter toute sorte de cle pendant l'execution de l'application
en faisant environ['session']['my_key'] = what_you_want

Moralite : on n'est jamais mieux servi que par soi-meme :-)

"""

class session_dict(dict):
    def __init__(self):
        self.data = {}
        self.modify = False
        
    def __setitem__(self, key, item):
#         print "#vv session -> set --> ", key, item
        self.data[key] = item
        self.modify = True
        
    def __getitem__(self, key):
#         print "#vv session -> get --> ", key
        return self.data[key]
    
    def has_key(self, key):
        return self.data.has_key(key)


import cPickle as pickle, sha, random
from pyson.pylib import framelib
from  pyson.middleware.cookie import Cookie

class Session:
    def __init__(self, application):
        self._application = Cookie(application)
        self.fd = None
        self.session = None
   
    def keygen(self):
        """Generateur de clef de 160 bits avec sha
       
        """
        chaine = "pkmCZggdfh5g5hO78IOt7yt\"\@ccs28xfFe0e68rxF6"
        sel = str(random.random())
        hashage = sha.new(chaine+sel);
        return hashage.hexdigest()
        
    def load_session(self, environ):        
        """ - Analyse des cookies
            - Chargement de la session si elle existe
            - la reference de self.session est mise dans le dico environ
        """
        if not environ.has_key('HTTP_COOKIE'):
            return False
        header_cookie = environ['HTTP_COOKIE']
        cookie = header_cookie.split('; ')
        for c in cookie:
            (name, value) = c.split('=')
            if len(value)  != 40:
                return False
            if not value.isalnum():
                return False
            
            if name == 'SID':
                try:
                    self.fd = open('/tmp/pyson_'+value)
                    self.session = pickle.load(self.fd)
                    self.fd.close()
                except IOError:
#                     print "#v Aucune session"
                    pass
                else:
                    environ['session'] = self.session 
                    return True
        return False
    
    def start_session(self, environ):
        """ - Verification de l'existence d'une session
            - sinon generation de clef
            - initialisation de la session
            - la reference de self.session est mise dans le dico environ
            - envoi du cookie avec l'id de la session
        """
        if self.load_session(environ):
            return
        value = self.keygen()
        try:
           
            self.session = session_dict()
            self.session['id'] = value
            self.session['_expires'] =  framelib.set_cookie(environ, 'SID', value,  '/', '',  604800)
            environ['session'] = self.session
            environ['session']['roles'] = ['visiteur']  #tous le monde est visiteur
            
        except:
            print "#v Impossible de creer session"
        
    
    def __call__(self, environ, start_response):
        
        
        self.start_session(environ)
        iterable =  self._application(environ, start_response)
        
        "on ecrit la session sur le disque que si la session a ete modifiee"
        if self.session.modify:
            try:
#                 print "#v serialisation", environ['session']
                self.fd = open('/tmp/pyson_'+ self.session['id'], 'w')
                self.session.modify = False
                pickle.dump(self.session, self.fd, pickle.HIGHEST_PROTOCOL)
                
            except IOError:
                print "#v Erreur lors de la creation de la session"
            self.fd.close()
            
        return iterable
