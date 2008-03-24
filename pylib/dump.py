from sqlobject import SQLObject
import os, sys, manage,zipfile, os.path, glob


def dumpDB(argv=''):
    """
    si '+db' : sauvgarde la Base de Donnee sous forme d'un fichier python 'dumpDB'
    puis cre un fichier zip contenant tout dans le dossier local de l'application
    @return: le nom du fichier compresse
    """
    import model, inspect
    try:
        fd = open('dumpDB', 'w')
    except IOError:
        print "Impossible de creer le fichier de sauvegarde"
        sys.exit(1)
        
    try:
        fd.write("#####Fichier de restauration de la base de donnees ######\nimport manage\nfrom model import *\nmanage.createdb(False)\n")
    except:
        print"Impossible d'ecrire dans le fichier dumpDB"
        sys.exit(1)
    
    if '+db' in argv:
        S = ""
        for (name, table) in vars(model).iteritems():
            if (inspect.isclass(table)) and (issubclass(table, SQLObject)) & (table != SQLObject):
                try:
                    if name.startswith('Assigned'):
                        S += createTable(name, table)
                    else:
                        fd.write(createTable(name, table))
                except IOError:
                    print"Impossible d'ecrire dans le fichier dumpDB"
                    sys.exit(1)
        fd.write(S)
        fd.close()
    nom = os.path.basename(os.getcwd())
    zipdirectory('../'+nom+'.zip', '../'+nom)
    return nom     




def createTable(name, table):
    t = table.select()
    S = ""
    for row in t:
        S += name + '('
        for col in row.sqlmeta.columnList:
            S += str(col.name) +'="'+ str(row.__dict__['_SO_val_'+str(col.name)])+'", '
        S +='id='+str(row.id)+')\n'
    return S
            
        
#source ----> http://python.developpez.com/faq/?page=Archive#ZipDir
def zipdirectory(filezip, pathzip):
    lenpathparent = len(pathzip)+1   ## utile si on veut stocker les chemins relatifs
    def _zipdirectory(zfile, path):
        for i in glob.glob(path+'/*'):
            if os.path.isdir(i): _zipdirectory(zfile, i )
            elif not i.endswith('~'):
                print i
                zfile.write(i, i[lenpathparent:]) ## zfile.write(i) pour stocker les chemins complets
    zfile = zipfile.ZipFile(filezip,'w',compression=zipfile.ZIP_DEFLATED)
    _zipdirectory(zfile, pathzip)
    zfile.close()

   
    
    
def restore():
    os.system('python dumpDB')
    
    
    
    
    





