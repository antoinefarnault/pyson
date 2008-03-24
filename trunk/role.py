"""
 Pour mettre un utilisateur dans un groupe il suffit d'utiliser les fonctions definies par SQLObject.
 Ex :
     user   = User(nom="lapin", prenom="jeannot", pseudo="jaja", password="C4rote")
     groupe = Groupe(nom="mamifere")

     user.addGroupe(groupe)
     groupe.addUser(user)

     user.removeGroupe(groupe)


     Pour afficher tout les utilisteur appartenant a un groupe
     groupe._users

     Pour afficher tout les groupes auxquel un utilisateur appartient
     user._groupes 
"""
# TODO:attention pour le moment les roles ne sont pris en compte qu'apres deconnexion et reconnexion
# car les session ne sont pas rafraichies......;

#  ------------------------
#   Ajouter ici vos roles
#  ------------------------

#def MonRole(environ, url):
#   start(environ, url,'/uneUrl')
#   start(environ, url, '/uneAutreUrl', False)

#  ---------------------------------
#   Roles predefinis
#  ---------------------------------

def admin(environ, url):
    start(environ, url, '/')


def visiteur(environ, url):
    start(environ, url,'/')
    start(environ, url, '/admin', False)
    contain(environ, url, '/add/', False)
    contain(environ, url, '/del/', False)
    contain(environ, url, '/mod/', False)

def start(environ, url, token, negation=True):
    if url.startswith(token):
        environ['permission'] = negation

def contain(environ, url, token, negation=True):
    if url.find(token) != -1:
        environ['permission'] = negation

def end(environ, url, token, negation=True):
    if url.endswith(token):
        environ['permission'] = negation

#creer un groupe
def createGroupe(name):
    Groupe(nom=name)

#creer role
def createRole(_role):
    Role(name=_role)
