from Cheetah.Template import Template
import context, os, model, inspect
from pyson.pylib.framelib import render
from pyson.pylib import forms,framelib, storage, dump
"""
    fonctions appelees par les redirrections d'urls
    les fonctions prennent en parametre :
        * environ
        * start_response
    les fonctions retournent au choix :
        + avec header et footer :
            * render(environ, start_response,'mon_template.html', locals())
        + sans header ni footer :
            * returnTemplate(environ, start_response,'mon_template.html', locals())
        + l'appel d'une autre fonction 
        + avec start_response("200 OK",[('Content-type', 'text/html')]) :
            * ["message a retourner"]
    """

def accueil(environ, start_response):
    header_     = "Yet another web framework..."
    title_      = "installation de pyson reussi"
    servername_ = context.conf["servername"]
    port_       = context.conf["port"]
    return  render(environ, start_response, 'accueil.html', locals())

def admin(environ,start_response):
    header_ = "Administration generales"
    title_  = "Interface d'administration"
    dojo_   = "1"
    webapps_= "1"
    return render(environ,start_response,'admin.html',locals())

def logs(environ,start_response):
    file    = open(context.conf["error_log"],"a") # TODO permettre de choisir entre error/debug/access
    logs_   = file.readlines()
    erreur_ = False
    if not logs_:
        erreur_ = True
    return returnTemplate(environ, start_response, 'logs.html', locals())
    
def post_users_add_del_groupe(environ, start_response):
    groupe = model.Groupe.select(model.Groupe.q.nom == environ['POST_GROUPE'])[0]#.
    user_count = 0
    start_response("200 OK", [('Content-type', 'text/html')])
    S='supprime/ajoute '
    for mini in environ:
        if mini.startswith('POST_'):
            if mini != 'POST_GROUPE' and mini != 'POST_RADIO_GROUPE':
                user = model.Users.select(model.Users.q.id == int(environ[mini]))[0]#.
                if environ['POST_RADIO_GROUPE'] == '1':
                    if not user in list(groupe._users):
                        groupe.addUsers(user)
                        user_count += 1
                        S = ' ajoute dans le'
                else:
                    if user in list(groupe._users):
                        groupe.removeUsers(user)
                        user_count += 1
                        S = ' supprime du' 
    return [str(user_count)+' utilisateur '+S+' groupe <q>'+groupe.nom+'</q>']

def post_groupes_add_del_role(environ, start_response):
    role = model.Role.select(model.Role.q.name == environ['POST_ROLE'])[0]#.
    groupe_count = 0
    start_response("200 OK", [('Content-type', 'text/html')])
    S='supprime/ajoute '
    for mini in environ:
        if mini.startswith('POST_'):
            if mini != 'POST_ROLE' and mini != 'POST_RADIO_ROLE':
                groupe = model.Groupe.select(model.Groupe.q.id == int(environ[mini]))[0]#.
                if environ['POST_RADIO_ROLE'] == '1':
                    if not groupe in list(role._groupes):
                        role.addGroupe(groupe)
                        groupe_count += 1
                        S = ' ajoute dans le' 
                else:
                    if groupe in list(role._groupes):
                        role.removeGroupe(groupe)
                        groupe_count += 1
                        S = 'supprime du '
    return [str(groupe_count)+' groupes '+S+' role <q>'+role.name+'</q>']
  

def insert(environ, table, comment="Operation effectuee"):
    dict = model.getKeyDict(table)
    S = "model."+table.__name__+"("
    for key in dict:
        S += key +"='" + environ['POST_'+key.upper()]+"', "
    S+= ")" 
    return eval(S)
    
def update(environ, table, element):
    p = table.select(table.q.id == int(element))[0]
    dict = model.getKeyDict(table)
    S = "p.set("
    for key in dict:
        S += key +"='" + environ['POST_'+key.upper()]+"', "
    S+= ")"    
    return eval(S) 
                   

def post_mod_table(environ, start_response):
    table = str(environ['selector.vars']['table'])
    table_obj = model.__dict__[table]
    update(environ, table_obj, environ['selector.vars']['name'])
    start_response("200 OK", [('Content-type', 'text/html')])
    return ["Operation effectuee avec succes"] 


def get_mod_table(environ, start_response):
    import types
    table = str(environ['selector.vars']['table'])
    name = str(environ['selector.vars']['name'])
    table_form = forms.__dict__[table]()
    table_obj = model.__dict__[table]
    
    S = 'javascript:post("/admin/table/mod/'+table+'/'+name+'", this.form.parentNode.getAttribute("id"), this.form)'
    table_form.submit.onclick = S
   
    response = table_obj.select(table_obj.q.id == int(environ['selector.vars']['name']))[0]#'
    
    #remplissage auto des champs
    for (name, val) in  inspect.getmembers(table_form):
        if type(val) is types.InstanceType and name != 'submit':
            if val.__class__ == forms.Input:
                val.value = response.__dict__['_SO_val_'+name]
            else:
                val._content = response.__dict__['_SO_val_'+name].replace('<br />', '\n')
    return returnTemplate(environ, start_response, '_add_table.html', locals())


    
    
def post_add_table(environ, start_response):
    from sqlobject import dberrors
    table = str(environ['selector.vars']['table'])
    start_response("200 OK", [('Content-type', 'text/html')])
    constraint = forms.__dict__[table]().constraint(environ)
    if constraint:
        framelib.set_err_info(environ, 'Formulaire', constraint)
        return  [constraint]
    try:
        insert(environ, model.__dict__[table])
    except dberrors.DuplicateEntryError:
        return ['Deja present dans la table']
    except:
        return['Operation failed ! ( ne pas mettre d\'accent pour le moment )']
    
    return [environ['selector.vars']['table']+"  ajoute avec succes"]

def get_add_table(environ, start_response):
    table = environ['selector.vars']['table']
    table_form = forms.__dict__[table]()
    S =  'javascript:post("/admin/table/add/'+table+'", this.form.parentNode.getAttribute("id"),this.form);'
    table_form.__class__.__dict__['submit'].onclick= S
    return returnTemplate(environ, start_response, '_add_table.html', locals())
    
def del_table(environ, start_response):
    table = environ['selector.vars']['table']
    table_obj = model.__dict__[table]
    table_obj.get(int(environ['selector.vars']['name'])).destroySelf()
    start_response("200 OK", [('Content-type', 'text/html')])
    return [table+" supprime"]

def roles(environ, start_response):
    roles_model = model.Role.select()
    return returnTemplate(environ, start_response,'role.html',locals())

def users(environ,start_response):
    users_model  = model.Users.select()
    groupe_model = model.Groupe.select()
    return returnTemplate(environ, start_response,'user.html',locals())

def info_user(environ, start_response):
    users_model   = model.Users.select(model.Users.q.id == int(environ['selector.vars']['user']))[0]#'
#     print "\n",dir(users_model.q),"\n"#,
    dict_user  = model.getKeyDict(model.Users)
    groupes_model = users_model._groupes
    return returnTemplate(environ, start_response,'info_user.html',locals())

def info_groupe(environ, start_response):
    groupe_model   = model.Groupe.select(model.Groupe.q.id == int(environ['selector.vars']['groupe']))[0]#'
    users_model = groupe_model._users
    roles_model = groupe_model._roles
    return returnTemplate(environ, start_response,'info_groupe.html',locals())
    
def groupes(environ, start_response):
    roles_model   = model.Role.select()
    groupes_model = model.Groupe.select()
    return returnTemplate(environ, start_response,'groupe.html',locals())

def upload(environ, start_response):
    from pyson.pylib import storage
    storage.create(environ['session']['pseudo'], environ['POST_FILE'].name, environ['POST_FILE_NAME'])
    try:
        environ['POST_FILE'].close()
    except OSError:#fichier deja supprime
        pass
    return admin(environ, start_response)#returnTemplate(environ,start_response,'admin.html',locals())
    #start_response("200 OK", [('Content-type', 'text/html')])
    #return []

def get_add_file(environ, start_response):
    return returnTemplate(environ,start_response,'add_file.html',locals())

def bdd(environ, start_response):
    tables = []
    for (name, table) in vars(model).iteritems():
        if (inspect.isclass(table)) and (issubclass(table, model.SQLObject)) & (table != model.SQLObject):
            if not name.startswith('Assigned'):
                tables.append(name)
    return returnTemplate(environ, start_response,'bd.html',locals())

def bdd_dump(environ, start_response):
    nom = dump.dumpDB('+db')
    storage.create(environ['session']['pseudo'], '../'+nom+'.zip', 'SAVE-'+nom+'.zip')
    start_response("200 OK", [('Content-type', 'text/html'), ('Charset', 'UTF-8')])
    return[]
   

def liste_table(environ, start_response):
    table = environ['selector.vars']['table']
    table_obj = model.__dict__[table]
    key = model.getKeyDict(table_obj)
    rows = table_obj.select()
    return returnTemplate(environ, start_response,'liste_table.html',locals())

def file(environ, start_response):
    pseudo = environ['session']['pseudo']
    if 'admin' in environ['session']['roles']:
        files = storage.search()
    else:
        files = storage.search(pseudo)
#     if not files:
#         start_response("200 OK", [('Content-type', 'text/html')])
#         return['Aucun ']
    return returnTemplate(environ, start_response,'file.html',locals())


def get_file(environ, start_response):
    pseudo = environ['session']['pseudo']
    if 'admin' in environ['session']['roles']:
        files = storage.search()
    else:
        files = storage.search(pseudo)
    return returnTemplate(environ, start_response,'get_file.html',locals())
    
def del_file(environ, start_response):
    key = environ["selector.vars"]["key"]
    storage.remove(key)
    files = storage.search()
    return returnTemplate(environ, start_response,'file.html',locals())
        

def returnTemplate(environ, start_response, templates, var):
    start_response("200 OK", [('Content-type', 'text/html'), ('Charset', 'UTF-8')])
    return Template(file=os.path.join('htdocs', 'templates', templates), namespaces=[var]).respond()

# def moved(start_response, dest):
#     start_response("302 Moved", [('Location', dest)])
#     return []

