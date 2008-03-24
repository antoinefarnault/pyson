"""
    Ce script lit le fichier de configuration ecrit sous la forme
    cle = "valeur" en sautant les commentaires.
    Il initialise un dictionnaire nomme conf.
"""


from os import environ
from sqlobject import *
import os, re, sys
# le dico qui contient les infos du fichier de conf
conf = {}

config_file = os.getcwd()+"/conf/pyson.conf"

# TODO :: permettre les commentaires en milieu de lignes
def read_conf_file():
    """ Cette fonction lit le fichier de configuration """
    
    if environ.has_key("PYSON_CONF"):
        install_dir = environ["PYSON_CONF"]
    else:
        install_dir = config_file
        file = open(install_dir,"r")
    
    lines  = file.readlines()
    for i in lines:
        if re.match("^[ \t]*#",i):   # on saute les commentaires
            continue
        conf_line = re.match("^\s*(\w*)\s*=\s*\"(.*)\"",i)
        if  conf_line:               # on ne prend que les lignes style aaa = "bbb"
            (key,val) = conf_line.groups()
            conf[key] = val
    file.close();

def print_conf():
    """cette fonction est faite pour des tests, (affiche la configuration)"""
    print "\nconf contient ["
    for key,value in conf.items():
        print "#vvv %s=%s" % (key, value)
    print "]"


def get_pyson_install_dir():
    """copie les fichiers dans /usr/lib/python{version}/site-packages ou dans le rep ecrit dans le fichier de configuration"""
    install_dir = None
    usr_lib_python = None
    for d in os.listdir("/usr/lib/"):
        if re.match(".*python.*",d):
            usr_lib_python = d
            break
    if usr_lib_python:
        install_dir = "/usr/lib/"+usr_lib_python+"/site-packages/pyson"
    return str(install_dir)




def set_default_value():
    """Les valeurs par defaut des cles indispensables"""
    if not conf.has_key("document_root"):
        conf["document_root"] = os.getcwd()+os.sep
    
    if not conf.has_key("header"):
        conf["header"] = "Pyson Framework"
     
    if not conf.has_key("port"):
        conf["port"] = "8080"
        
    if not conf.has_key("title"):
        conf["title"] = "Pyson Framework"
        
    if not conf.has_key("auteur"):
        conf["auteur"] = "pyson team"
        
    if not conf.has_key("sgbd"):
        conf["sgbd"] = "sqlite"
        
    if not conf.has_key("host_bdd"):
        conf["host_bdd"] = "localhost"      
        
    if not conf.has_key("nom_bdd"):
        conf["nom_bdd"] = "myblog.db"
        
    if not conf.has_key("user_bdd"):
        conf["user_bdd"] = "user"
        
    if not conf.has_key("pass_bdd"):
        conf["pass_bdd"] = "pass"
        
    if not conf.has_key("debug"):
        conf["debug"] = "false"
    
    if not conf.has_key("verbose"):
        conf["verbose"] = "v"
    
    if not conf.has_key("access_log"):
        conf["access_log"] = "/var/log/pyson_access.log"

    if not conf.has_key("error_log"):
        conf["error_log"] = "/var/log/pyson_error.log"

    if not conf.has_key("debug_log"):
        conf["debug_log"] = "/var/log/pyson_debug.log"
        
    if not conf.has_key("tmp"):
        conf["tmp"] = "/tmp"
        
    if not conf.has_key('install_dir'):
        conf['install_dir'] =    get_pyson_install_dir() 
        
def set_python_path():
    """ cette fonction ajoute document_root et pylib dans le python path"""
    sys.path.append(conf["document_root"])
    sys.path.append(conf["document_root"]+"/pylib")

def set_bdd_conn():
    """Cette fonction initialise la connexion a la base de donnee en fonction du sgbd choisit
    """
    if conf.has_key("sgbd"):
#         print "#vv connection a la base de donnee"
        if conf["sgbd"] == "sqlite":
#             print "#vvv utilisation de sqlite"
            conf["connection_bdd"] = "sqlite://"+os.getcwd()+os.sep+conf["nom_bdd"]
            sqlhub.processConnection = connectionForURI(conf["connection_bdd"])
            
        if conf["sgbd"] == "mysql":
#             print "#vvv utilisation de mysql"
            if conf.has_key("pass_bdd"):
#                 print "mysql://"+conf["user_bdd"]+":"+conf["pass_bdd"]+"@"+conf["host_bdd"]+"/"+conf["nom_bdd"]
		sqlhub.processConnection = connectionForURI("mysql://"+conf["user_bdd"]+":"+conf["pass_bdd"]+"@"+conf["host_bdd"]+"/"+conf["nom_bdd"])
            else:
                sqlhub.processConnection = connectionForURI("mysql://"+conf["user_bdd"]+":@"+conf["host_bdd"]+"/"+conf["nom_bdd"])
                
        if conf["sgbd"] == "postgresql":
#             print "#vvv utilisation de postgresql"
            if conf.has_key("pass_bdd"):
                sqlhub.processConnection = connectionForURI("postgres://"+conf["user_bdd"]+":"+conf["pass_bdd"]+"@"+conf["host_bdd"]+"/"+conf["nom_bdd"])
            else:
#                 print "hehe"
                sqlhub.processConnection = connectionForURI("postgres://"+conf["user_bdd"]+":@"+conf["host_bdd"]+"/"+conf["nom_bdd"])

# lecture & initialisation
read_conf_file()
set_default_value()
#print_conf()

# initialisation du contexte d'execution
# set_python_path()
set_bdd_conn()
