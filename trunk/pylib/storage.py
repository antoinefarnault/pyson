import bsddb, os, md5, time, random, shutil, os.path
"""
    gestion du FilesPool avec une base berkeley
    et les fonctions suivantes :
        * create(user,path,name)
        * remove(key)
        * file(key)
        * find(lile,user)   user optionnel
        * search(user)      user optionnel
    creation a la racine du Dossier FilesPool/
    """

folder = 'FilesPool/'
if not os.path.exists(folder):
    os.mkdir(folder)

def create(user, path, name):
    """
    insere un fichier 'name' dans le FilesPool
    se trouvant dans 'path' ce fichier appartien a l'utilisateur 'user'
    """
    db = bsddb.btopen(folder+'index.db', 'c')
    if not os.path.exists(path):
        raise("Le fichier n'existe pas")
    
    basename = name
    basename = basename.replace('_', '')
    #on supprime les '_' du user
    user = user.replace('_', '')
    
    #generation de la cle de la base berkeley
    key  = user+'_'+str(random.getrandbits(30))+'_'+basename
    while db.get(key):
        key  = user+'_'+str(random.getrandbits(30))+'_'+basename

    #generation du chemin dans l'arborescence
    hash = md5.new(key).hexdigest()
    hash = hash[:4]+'/'+hash[4:8]+'/'+hash[8:]
    while os.path.exists(folder+hash):
        hash = md5.new(key+random.getrandbits(30)).hexdigest()
        hash = hash[:4]+'/'+hash[4:8]+'/'+hash[8:]
         
    #creation du fichier      
    os.makedirs(folder+hash[:10])
#     print 'path=', path, 'folder+hash=', folder+hash
    #attention copy de shutil pose probleme !
    os.rename(path, folder+hash)
    
    #sauvegarde du chemin dans la base berkeley
    db[key] = hash
    db.close()

def remove(key):
    """
    suprime du FilesPool le fichier correspondant a 'key'
    """
    db = bsddb.btopen(folder+'index.db', 'w')
    try:
        os.unlink(os.path.join('FilesPool', db[key]))
    except:
        print "Impossible de supprimer le fichier"
    if db.has_key(key):
        db[key] = None
    db.close()

def file(key):
    """
    renvoi le path du fichier rechercher suivant la 'key'
    """
    db = bsddb.btopen(folder+'index.db', 'r')
    try:
        return db[key]
    except:
        return False


def find(file, user=''):
    """
    permet de rechercher tout les fichiers nomes 'file' du FilesPool
    en donnant un nom d'utilisateur optionnel, ne sera renvoye que
    les fichiers nomes 'file' appartenant a cet utilisateur
    """
    try :
        db = bsddb.btopen(folder+'index.db', 'r')
    except bsddb._db.DBNoSuchFileError :
        return []
    result = map(lambda x: (x, x.split('_')[2]) , filter(lambda x: ((x.split('_')[2] == file ) and (x.startswith(user)) and (db[x]) ), db.keys()))
    db.close()
    return result


def search(user=''):
    """
    permet de rechercher tout les fichiers du FilesPool
    en donnant un nom d'utilisateur optionnel, ne sera renvoye que
    les fichiers appartenant a cet utilisateur
    @return: une liste de doubles [(key1,nom1),(key2,nom2),...]
    """
    try :
        db = bsddb.btopen(folder+'index.db', 'r')
    except bsddb._db.DBNoSuchFileError :
        return []
    result =  map(lambda x: (x, x.split('_')[2]) , filter(lambda x: ((x.startswith(user)) and (db[x]) ), db.keys()))
    db.close()
    return result









