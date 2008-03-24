"""Auth - permet l'authentification des utilisateurs

l'authentification des utilisateurs se fait dans la table user

"""

import os, view, model
from pyson.pylib import framelib, forms

def logout(environ, start_response):
    framelib.set_cookie(environ, 'SID', '',  '/', '',  -1)
    try:
        os.unlink('/tmp/pyson_'+environ['session']['id'])
    except:
        print 'Impossible de supprimer la session ', '/tmp/pyson_' + environ['session']['id']
    start_response("302 Moved", [('Location', '/')])
    return []
   

def open_session(environ, username,password):
    from model import AND, Users
    rows = model.Users.select(AND(Users.q.pseudo==username, Users.q.password==password))
    if rows.count() == 1:
        for row in rows:
            #Optimisation - si pas de changement pas de reecriture (un test vaut mieux qu'une ecriture.....)
            #car quand un chgmt est detectee dans le dico de session ---> re-serialisation
            # 'or' plutot que '|' pour n'evaluer la deuxieme condition seulement si la premiere est fausse
            if not (environ['session'].has_key('auth')) or (row.pseudo != environ['session']['pseudo']):
                environ['session']['auth'] = True
                environ['session']['pseudo'] = row.pseudo
                environ['session']['nom'] = row.nom
                environ['session']['prenom'] = row.prenom
#                 environ['session']['roles'] = ['visiteur'] --> deplace dans session.py
                for groupe in row._groupes:
                    roles =  groupe._roles
                    for role in roles:
                        environ['session']['roles'].append(role.name)
                        
                 
        return True
    return False





def authentification(environ, start_response):
    password = environ['POST_PWD']
    username = environ['POST_LOGIN']
#     print environ['POST_LOGIN'], environ['POST_PWD']
    constraint = forms.Login().constraint(environ)
    if constraint:
        framelib.set_err_info(environ, 'Formulaire', constraint)
        return  login(environ, start_response)
    
    if open_session(environ, username, password):
        if 'logout' in environ['PATH_INFO']:
            start_response("302 Moved", [('Location', '/')])
        else:
            start_response("302 Moved", [('Location', '/'+environ['PATH_INFO'].replace('/login', ''))])
        return []
    else:
        framelib.set_err_info(environ, 'Identification', 'Mot de passe ou login incorect')
        return  login(environ, start_response, environ['PATH_INFO'])
    
    
def login(environ, start_response, path="/"):
    header_ = "Identifiez vous"
    title_  = "Identification pyson"
    #Pas de javascript au login ---> onsubmit=""
    login = forms.Login(onsubmit="")
    return framelib.render(environ, start_response, 'login.html', locals())







