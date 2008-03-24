import selector, os, view, context
from pyson.pylib import static, auth
from Cheetah.Template import Template
"""
    redirrection des urls.
    
    appel des fonctions de view suivant les urls demanees
    urls.add('/mon/url/a_ratraper',GET=view.ma_fonction1,POST=view.ma_fonction2)
    POST et GET sont optionnels
    
    pour les urls dynamiques des arguments sont possibles.
    urls.add('/url/{arg1}/{arg2},GET=...,POST=...)
    les variables 'arg1' et 'arg2' seront envoyees a la fonction appelee
    
    les urls peuvent etre des expressions regulieres
    urls.add('.*?/url/(?P<arg1>.+?)/(?P<arg2>[^/]+$)',GET=...,POST=...)
    les variables 'arg1' et 'arg2' seront envoyees a la fonction appelee
    """
class Selector(selector.Selector):

    def not_found(self, environ, start_response):
        var = {}
        var['error'] = ''
        start_response("404 NOT FOUND", [('Content-Type', 'text/html')])
        return Template(file=os.path.join('htdocs', 'templates', '404.html'), namespaces=[var]).respond() 
    status404 = not_found

urls = Selector()

urls.add('/', GET=view.accueil)
urls.add('/logout', GET=auth.logout)
urls.add('/admin', GET=view.admin)
# urls.add('/login', GET=auth.login)

urls.add('/admin/log', GET=view.logs)
urls.add('/admin/Users', GET=view.users)
urls.add('/admin/Role', GET=view.roles)
urls.add('/admin/Groupe', GET=view.groupes)
urls.add('/admin/file', GET=view.file)
urls.add('/admin/file/add', GET=view.get_add_file,POST=view.upload)

urls.add('/get/file', GET=view.get_file)

urls.add('/admin/bdd', GET=view.bdd)
urls.add('/admin/bdd/dump', GET=view.bdd_dump)


urls.add('/admin/Users/{user}', GET=view.info_user)
urls.add('/admin/Groupe/{groupe}', GET=view.info_groupe)


urls.add('/admin/users/add_del_groupe', POST= view.post_users_add_del_groupe)
urls.add('/admin/groupes/add_del_role', POST=view.post_groupes_add_del_role)



"""Attention apres cette ligne des expressions regulieres devront 
etre utilisee dans la methode add
"""
sauve = urls.parser

urls.parser = lambda x: x
  
urls.add('^/static(?P<path>/.*)', GET=static.StaticFile)
urls.add('^/login(?P<path>.*)', GET=auth.login, POST=auth.authentification)
urls.add('^/admin/file/del/(?P<key>.+)', GET=view.del_file)

urls.add('/table/add/(?P<table>[^/]+$)', GET=view.get_add_table, POST=view.post_add_table)
urls.add('/table/liste/(?P<table>[^/]+$)', GET=view.liste_table)
urls.add('/table/mod/(?P<table>.+?)/(?P<name>[^/]+$)', GET=view.get_mod_table, POST=view.post_mod_table)
urls.add('/table/del/(?P<table>.+?)/(?P<name>[^/]+$)', GET=view.del_table)

urls.parser = sauve
