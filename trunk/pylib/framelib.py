from Cheetah.Template import Template
import os, context

def render(environ, start_response, template_file, var, directory=''):
    """Fonction executant start_response, c'est a dire renvoi la requete au serveur
    qui la transmet au client. (en wsgi l'application discute en local avec le serveur)
    """
    body   = Template(file=os.path.join('htdocs', 'templates', template_file), namespaces=[var, environ])
    footer = Template(file=os.path.join('htdocs','templates', 'footer.html'))
    status =  '200 OK'

    "mise en place des headers_http"
    header_http = [('Content-Type', 'text/html'), ('Charset', 'UTF-8')]
    start_response(status, header_http)
    return [set_header_html(var), body.respond(), footer.respond()]

def set_header_html(var):
    """Cette fonction ajoute les headers_html par defaut Doctype, <html><head>....
    Elle permet aussi la redefinition de title de la fenetre et du titre du site
    """
    import types
    if not 'header_' in var:
        var['header_'] = context.conf["header"]
    if not 'title_' in var:
        var['title_'] =  context.conf["title"]
    if not 'style_' in var:
        var['style_'] = []
    else:
        if not type(var['style_']) is types.ListType:
            raise 'style_ doit etre de type list'

    if not 'menu_lateral' in var:
        menu_lateral = get_menu_latteral()
#         menu_lateral = {}
#         menu_lateral['site officiel'] = 'http://pyson.org'
#         menu_lateral['documentation'] = 'http://pyson.org/doc.php'
#         menu_lateral['wiki']          = 'http://pyson.org/wiki/'
#         menu_lateral['depot svn']     = 'http://viewvc.tuxfamily.org/svn_pyson_pyson/'
#         menu_lateral['apropos']       = 'http://pyson.org/contact.php'
#         var['menu_lateral'] = menu_lateral
    var['menu_lateral'] = menu_lateral
    
    if not 'dojo_' in var:
        var['dojo_'] = False
    else:
        var['dojo_'] = True

    return Template(file=os.path.join('htdocs','templates', 'header.html'), namespaces=[var]).respond()

def get_menu_latteral():
    import re
    menu_lateral = {}
    for k in context.conf.keys():
        menu = re.match("menu\d",k)
        if menu:
            label_url = re.search("\s*([\w\s]*)-->\s*([\w\/]*)\s*",context.conf[k])
            (label,url) = label_url.groups()
            menu_lateral[label] = url
    
    return menu_lateral


def get_cookie(environ):
    """fonction recuperant les cookies dans la variable environ.
    Cette fonction est iterative et renvoi un par un les cookies
    envoyes par le client
    """
    if not environ.has_key('HTTP_COOKIE'):
        return
    header_cookie = environ['HTTP_COOKIE']
    cookie = header_cookie.split('; ')
    for c in cookie:
        yield c

def set_cookie(environ, name, value,  path, domain,  expires):
    """Permet d'envoyer un cookie au moment au les headers sont envoyes.
    expires est le temps en secondes depuis la date courante
    """
    from time import strftime, gmtime, mktime, localtime
    expires = strftime("%a, %d-%b-%Y %H:%M:%S GMT", gmtime(mktime(localtime())+expires))

    if not environ.has_key('set_cookie'):
        environ['set_cookie'] = []
    cookie = "%s=%s; path=%s; expires=%s; domain=%s" % (name, value, path, expires, domain)
    environ['set_cookie'].append(('Set-Cookie', cookie))
    return expires

def send_404(start_response, error=''):
    var = {}
    var['error'] = error
    start_response("404 NOT FOUND", [('Content-Type', 'text/html')])
    return Template(file=os.path.join('htdocs', 'templates', '404.html'), namespaces=[var]).respond()

#sert a stocker un ou plusieurs message d'erreur a  afciher sur la page
def set_err_info(environ, titre, description):
    err_info = environ.get('err_info')
    if err_info:
        err_info.append((titre, description))
    else:
        environ['err_info'] = [(titre, description)]

def get_err_info(environ):
    err_info = environ.get('err_info')
    if err_info:
        return err_info
    return False

