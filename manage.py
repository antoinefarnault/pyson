#!/usr/bin/env python
"""Manage - Module de management du framework

Ce module permet creer les tables dans la base de donnee
et de lancer un serveur wsgi
"""

import sys, os, urls


import context, inspect
from pyson.pylib import framelib, forms


def createdb(init=True):
    """creer la base de donnee
    a partir de la liste des tables presentent dans le module
    models
    """
    import model
    from sqlobject import SQLObject, sqlhub
    from model import Users, Groupe, Role 
    
    constraints = []
        
    for (name, table) in vars(model).iteritems():
        if (inspect.isclass(table)) and (issubclass(table, SQLObject)) & (table != SQLObject):
            if context.conf["sgbd"] == "postgresql":
                constraints.extend(table.createTable(applyConstraints=False, ifNotExists=True)) # True pour ne pas creer la table si elle existe deja
            else:
                table.createTable(ifNotExists=True)   
            print "Creation de la table `"+name+'` OK'
    
    
    # Les contraintes ne sont ajoute qu'a la fin (pour postgresql)
    if context.conf["sgbd"] == "postgresql":
        if constraints:
            for constraint in constraints:
                if constraint:
                    sqlhub.processConnection.query(constraint)
    if not init:
        return 
    
    #ajout d'un groupe par default, role et association (ne rien faire si il existe deja)
    if not list(Groupe.select(Groupe.q.nom=='visiteur')):#.
        groupe = Groupe(nom="visiteur")
    if not list(Role.select(Role.q.name=='visiteur')):#.
        role = Role(name="visiteur")
        groupe.addRole(role)
    
    #Ajout d'un groupe admin et d'un admin (ne rien faire si il existe deja)
    if not list(Users.select(Users.q.pseudo=='admin')):#.
        user = Users(nom="", prenom="", pseudo="admin", password="nimda")
        print "\n--> Creation d'un compte `admin` mot de passe : `nimda`" 
        groupe = Groupe(nom="admin")
        role   = Role(name="admin")
        groupe.addRole(role)
        user.addGroupe(groupe)

    print "Tables crees avec succes\n"   
           
 
def runserver():
    """Lance un serveur wsgi de test, puis lui attribue l'application a
    lancer avec eventuellement le chainage de middleware
    """
    from pyson.middleware.error   import HandleError
    from pyson.middleware.log     import Log
    from pyson.middleware.session import Session  #se wrapp automatiquement avec cookie
    from pyson.middleware.force_auth import Force_auth
    from pyson.middleware.http_basic import Http_basic
    from pyson.middleware.formdata import Formdata
    from pyson.middleware.restriction import Middle as Restriction 

    if os.environ.get("REQUEST_METHOD", ""):
        from wsgiref.handlers import BaseCGIHandler
        BaseCGIHandler(sys.stdin, sys.stdout, sys.stderr, os.environ).run(urls.urls)
        print "-------------  Attention ---------------"
    else:
        import wsgiref
        from wsgiref.simple_server import WSGIServer, WSGIRequestHandler
        httpd = WSGIServer(('', int(context.conf["port"])), WSGIRequestHandler)

        wrapper  = Session(Formdata((Restriction(urls.urls))))

        httpd.set_app(wrapper)

        print "Serving HTTP on %s port %s ..." % httpd.socket.getsockname()
        httpd.serve_forever()

def shell():
    """met a disposition un shell python
    avec une autocompletion
    """
    os.system("python -i -c 'import manage\nimport rlcompleter\nimport readline\nreadline.parse_and_bind(\"tab: complete\")'")

def sql():
    """ permet d'acceder a un shell sql
    """
    if context.conf["sgbd"] == "sqlite":
#         print "#vv ouverture shell sqlite"
#         print "#vvv sqlite3 "+context.conf['nom_bdd']
        os.system("sqlite3 "+context.conf["nom_bdd"])
        
    if context.conf["sgbd"] == "mysql":
#         print "#vv ouverture shell mysql"
#         print "#vvv mysql -u"+context.conf["user_bdd"]+" -p"+context.conf["pass_bdd"]+" --database "+context.conf["nom_bdd"]
        os.system("mysql -u"+context.conf["user_bdd"]+" -p"+context.conf["pass_bdd"]+" --database "+context.conf["nom_bdd"])
        
    if context.conf["sgbd"] == "postgresql":
#         print "#vv ouverture shell psql"
#         print "psql -U"+context.conf["user_bdd"]+" -d "+context.conf["nom_bdd"]
        os.system("psql -U"+context.conf["user_bdd"]+" -d "+context.conf["nom_bdd"])

def createforms():
    forms.formsAuto()

if __name__ == "__main__":
    if 'createdb' in sys.argv:
        createdb()
        createforms()
        sys.exit()
    if 'runserver' in sys.argv:
        runserver()
        sys.exit()
    if 'shell' in sys.argv:
        shell()
        sys.exit()
    if 'dump' in sys.argv:
        from pyson.pylib import dump
        dump.dumpDB(sys.argv)
        sys.exit()
    if 'sql' in sys.argv:
        sql()
        sys.exit()
    if 'restore' in sys.argv:
        from pyson.pylib import dump
        dump.restore()
        sys.exit()
    if 'createforms' in sys.argv:
        createforms()
        sys.exit()
    print "cette commande n'existe pas"
    
