# -*- coding: latin1 -*-
""" FormData - Traitement des post de formulaire

Pris sur le site officiel : http://www.wsgi.org/wsgi/Specifications/handling_post_forms
...et au passage un bug corrige ;)

"""
import cgi, tempfile

def filter(chaine, admin=False):
    chaine = str(chaine).strip()
    
    if not admin:
        chaine = cgi.escape(chaine, True)
    
    chaine =chaine.replace("'", "\\'")
    chaine = chaine.replace('\n', '<br />')
    return chaine


def is_post_request(environ):
    if environ['REQUEST_METHOD'].upper() != 'POST':
        return False
    content_type = environ.get('CONTENT_TYPE', 'application/x-www-form-urlencoded')
    return (content_type.startswith('application/x-www-form-urlencoded') or (content_type.startswith('multipart/form-data')))

def is_get_request(environ):
    if environ['REQUEST_METHOD'].upper() != 'GET':
        return False
    return True


def get_post_form(environ):
    assert is_post_request(environ)
    input = environ['wsgi.input']
    post_form = environ.get('wsgi.post_form')
    if (post_form is not None
        and post_form[0] is input):
        return post_form[2]
    # This must be done to avoid a bug in cgi.FieldStorage
    environ.setdefault('QUERY_STRING', '')
    fs = cgi.FieldStorage(fp=input,
                          environ=environ,
                          keep_blank_values=1)
    new_input = InputProcessed()
    post_form = (new_input, input, fs)
    
    if environ['CONTENT_TYPE'].startswith('application/x-www-form-urlencoded'):
        environ['wsgi.post_form'] = post_form
        environ['wsgi.input'] = new_input
        fieldstorage = environ['wsgi.post_form'][2]
        for i in fieldstorage.list:
            if 'admin' in environ['session']['roles']:
                environ['POST_'+i.name.upper()] = filter(i.value, True)
            else: 
                environ['POST_'+filter(i.name).upper()] = filter(i.value)
    elif environ['CONTENT_TYPE'].startswith('multipart/form-data'):
        tmp_file = tempfile.NamedTemporaryFile()
        tmp_file.write(fs['file'].file.read())
        environ['POST_FILE'] = tmp_file
        environ['POST_FILE_NAME'] = fs['file'].filename
        

    
    return fs


def get_get(environ):
    assert is_get_request(environ)
    if not environ['QUERY_STRING']:
        return 
    get = environ['QUERY_STRING'].split('&')
    for item in get:
        item = item.split('=')
        environ['GET_'+filter(item[0]).upper()] = filter(item[1])


class InputProcessed(object):
    def read(self, *args):
        raise EOFError('The wsgi.input stream has already been consumed')
    readline = readlines = __iter__ = read
    
    

class Formdata:
    def __init__(self, application):
        self.application = application
        
    def __call__(self, environ, start_response):
        if is_post_request(environ):
            get_post_form(environ)
        if is_get_request(environ):
            get_get(environ)
        return self.application(environ, start_response)
        









