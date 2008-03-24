""" Error - Middleware de rattrapage d'exception

Si le flag debug du fichier de conf est a True
les exceptions seront rattrapees

"""
import sys, traceback, context

class HandleError:
    """Classe de rattrapage d'erreur
    """
    def __init__(self, application):
        self._application = application
        
    
    def print_file(self, file, line):
        """Affiche le code contenant l'erreur
        """
        self._file = file
        self._line = line
        try:
            self._file = open(file)
        except IOError:
            print "can't open", file   
        
        n = 0
        retour ="....\n"
        for line in self._file:
            n +=1
            if (self._line-5 < n) &  (n < self._line+5) & (n !=  self._line):
                retour += line
            if n ==  self._line:
                retour += ("<font color='red'><b>%s</b></font>" % (line))
        
        return retour + "...."
        self._file.close()
        
       
    def error(self, environ, start_response):
        """Affiche les informations de debuggage
        """
        
        "Generate an error report"
        status = '200 Handle error'
        headers = [('Content-type','text/html')]
        start_response(status, headers)
        trace = traceback.extract_tb(sys.exc_traceback)
        return ['Error<br />[Exception] <i><q>%s</q></i> <br /> [File ] <i><q>%s</q></i> <br /><pre>%s</pre>'
                % (sys.exc_info()[0],trace[-1][0],self.print_file(trace[-1][0], trace[-1][1]))]
            
            
    def __call__(self, environ, start_response):
        if (context.conf["debug"] == "true"):
            try:
                return self._application(environ, start_response)
            except:
                return self.error(environ, start_response)
        else:
            return self._application(environ, start_response)
