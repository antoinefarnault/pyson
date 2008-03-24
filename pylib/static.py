import mimetypes, re, os
import framelib
"""
    permet d'avoir un acces dirrect aux fichiers
    """
    
#  TODO
#  Une uniformisation de la maniere de traiter les chemins est a faire
#  Quand la nouvelle version de settings sera prete il faudra l'utiliser pour
#  ca et faire de meme partout

def StaticFile(environ ,start_response):
#     path = environ['selector.vars']['path']
    path = environ['SCRIPT_NAME']
    if not path:
        path = environ['PATH_INFO']
    
    #on trrouve le content-type
    content_type = mimetypes.guess_type(path)[0]
    
    if path.startswith('/static/htdocs'):
        path = path.split('/static/')[1]
    elif path.startswith('/static/FilesPool'):
        path = path.split('/static/')[1]#permet de telecharger le fichier avec son vrai nom
        path = "/".join(path.split('/')[:4])
#         print path
    else:
        return framelib.send_404(start_response, "Syntaxe de l'url incorrecte")   
       
    if path  == '':
        return framelib.send_404(start_response, 'Chemin incomplet')
    
    if len(path) > 150:
        return framelib.send_404(start_response, 'URL depassant la taille limite')

    if (re.search('\.{2,}', path)):
        return framelib.send_404(start_response, "Syntaxe de l'url incorrecte")
    
    if (re.search('^\.', path)):
        return framelib.send_404(start_response, "Syntaxe de l'url incorrecte")
    
    #on match tous les py, py~, pyc, .conf
#     print path
    if (path.find('.py') != -1) | (path.find('.conf') != -1):
        return framelib.send_404(start_response, "Syntaxe de l'url incorrecte")
    
    
    if not content_type:
        content_type = 'text/pyson'
    try:
        fd = open('./'+(path))
    except:
        return framelib.send_404(start_response, '')
    else:
        start_response("200 OK", [('Content-Type', content_type)])
        return fd



