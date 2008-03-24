import sys
sys.path.append("pylib/")
import shutil, context, os, re, sys

pyson_inst_bin = "/usr/bin" # FIXME :: non portable

def get_install_dir():
    """copie les fichiers dans /usr/lib/python{version}/site-packages ou dans le rep ecrit dans le fichier de configuration"""
    usr_lib_python = None
    install_dir = None
    if context.conf.has_key('INSTALL_DIR'):
        install_dir = context.conf['INSTALL_DIR']
    else:
        #for d in os.listdir("/usr/lib/"):
        #    if re.match("^python2\.[\d]{1}",d):
        #        usr_lib_python = d
        if '/usr/lib/python2.5' in sys.path:
            usr_lib_python = 'python2.5'
        elif '/usr/lib/python2.4' in sys.path:
	    usr_lib_python = 'python2.4'
	else:
            print "incapable de determiner le rep d'install"
        try:
            os.makedirs("/usr/lib/"+usr_lib_python+"/site-packages")
        except OSError, e:
	    pass
#                 break
        if usr_lib_python:
            install_dir = "/usr/lib/"+usr_lib_python+"/site-packages/"
    return str(install_dir)

def install_enable(install_dir):
    """Verifie si l'utilisateur courant a le droit d'installer dans install_dir"""
    if os.access('/'+install_dir.split('/')[1],os.W_OK):
        return True
    return False

def copytree(src, dst, symlinks=0):
    names = os.listdir(src)
    os.mkdir(dst)
    for name in names:
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        try:
            if symlinks and os.path.islink(srcname):
                linkto = os.readlink(srcname)
                os.symlink(linkto, dstname)
            elif os.path.isdir(srcname):
                if not (srcname.endswith('.svn') | srcname.endswith("scripts")):
                    copytree(srcname, dstname, symlinks)
            else:
                if not((srcname.endswith('~'))):
                    shutil.copy2(srcname, dstname)
                    
        except (IOError, os.error), why:
            print "Can't copy %s to %s: %s" % (`srcname`, `dstname`, str(why))

def create_install_dir(install_dir):
    try:
        os.makedirs(install_dir)
    except:
        pass

def _help():
    return "usage :\n\tpython setup.py build   - Pour compiler les modules\n\tpython setup.py install - Pour installer"

if __name__ == "__main__":
    if 'install' in sys.argv:
        install_dir = get_install_dir()
        print "installation dans "+install_dir+"\n"
        if not install_dir:
            print "repertoire d'installation non trouve"
            exit
            
        if install_enable(install_dir):
            print "\n\nInstallation en cours...\n\n"
            copytree('.',install_dir+'/pyson')
            #copie des scripts dans le path
            os.chmod("scripts/pyson", 0755)
            shutil.copy2("scripts/pyson",pyson_inst_bin)
        else:
            print "L'utilisateur courant semble ne pas avoir le droit d'ecrire dans "+install_dir
        sys.exit()
    if 'build' in sys.argv:
        "on importe tout pour compiler"
        # TODO :: voir comment ca marche....
        sys.exit()
    
    sys.exit(_help())   
        
