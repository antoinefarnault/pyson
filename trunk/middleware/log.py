""" log - Gestion des logs


"""
import context, os, sys, re, time, string

class StandardOutput:
    """classe permettant de faire des logs suivant plusieurs regles. Ex :
        - print '#v Hello les gars'
        Marquera (v) Hello les gars dans le fichier debug.log si le mode est verbeux simple (v), moyen (vv) ou fort (vvv)
        
        - print '#vvv Hello lapin'
        Marquera (vvv) Hello lapin uniquement si le mode est verbuex fort(vvv)
        
        - print 'coucou' marquera coucou sur la sortie standard
        
        Par default toute les requetes sont logguees dans le fichier access.log 
        Toutes les erreurs (stderr) sont redirigees vers le fichier error.log   :-)
        
    """
    def __init__(self, environ, fs_access, fs_debug, saveout):
        self.fs_access = fs_access
        self.fs_debug = fs_debug
        self.verbose = context.conf['verbose']    #sera par la suite lu dans le fichier de configuration
        self.isLog = re.compile('^(#)')
        self.isDebug = re.compile('^#([v]{,%s})[ ]+(.*)' % (len(self.verbose)), re.IGNORECASE)
        self.saveout = saveout
        self.environ = environ
        self.date = time.strftime("%a, %d-%b-%Y %H:%M:%S GMT", time.gmtime(time.mktime(time.localtime())))
        self.first = True
        
    def write(self,  out):
        """cette fonction est appellee a chaque print dans le programme.
        Elle verifie ce qui est ecrit pour savoir quoi logguer ou non
        NB : cette fonction ne doit pas faire de print
        """
        
        self.fs_access.write("%s  %s  %s  %s:%s  %s  %s\n" %        (self.environ['REQUEST_METHOD'], self.environ['PATH_INFO'], self.environ['SERVER_PROTOCOL'],        self.environ['HOSTNAME'],
self.environ['SERVER_PORT'], self.environ['REMOTE_ADDR'], self.date))
        
        
        debug = self.isDebug.match(out)
        log = self.isLog.match(out)
        
        if log:
            if debug:
                if self.first:
                    self.fs_debug.write(self.date+" :\n")
                    self.first = False
                self.fs_debug.write(string.ljust("("+debug.group(1)+")", 6)+debug.group(2)+"\n")
        else:
            self.saveout.write(out)

class Log:
    def __init__(self, application):
        self._application = application
   
    def __call__(self, environ, start_response):
#         print "coucou"
        saveout = sys.stdout
        saverr  = sys.stderr
        
        fs_access = open(os.path.join("", context.conf["access_log"]), 'a')
        fs_debug  = open(os.path.join("", context.conf["debug_log"]), 'a')
        fs_err    = open(os.path.join("", context.conf["error_log"]), 'a')
                
        sys.stdout = StandardOutput(environ, fs_access, fs_debug, saveout)
        sys.stderr = fs_err
        
        print ''
        
        iterable =  self._application(environ, start_response)
        
#         fs_debug.write('\n\n')
        
        fs_access.close()
        fs_debug.close()
        fs_err.close()
        
        sys.stdout = saveout
        sys.stderr = saverr
        return iterable
        
