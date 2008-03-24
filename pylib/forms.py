import inspect, re, sys, os.path
"""
    les formulaires sont generes automatiquement par 'formsAuto'
    possibilite de rajouter des contraintes a ces formulaires :
        integrer dans la class :
        def constraint(self, environ):
            if fonctionDeCondition1(environ,'champ1'):
                return 'message de contrainte 1'
            if fonctionDeCondition2(environ,'champ2'):
                return 'message de contrainte 2'
    """


if not os.path.exists('formulaire.py'):
    if not 'createforms' in sys.argv:
        print "Aucun formulaire genere. Executer ./manage.py createforms\n--> Ceci effacera les anciens"
        sys.exit(0)


def popKey(kw, name, default=None):
    if not kw.has_key(name):
        return default
    value = kw[name]
    del kw[name]
    return value

class main:
    def set_label(self):
        return "\n<dt><label for='%s'>%s</label></dt>\n<dd>%s</dd>" % (self.id, self._label, self)

class Input(main):
    def __init__(self, **kw):
        """Tout est la --> http://www.w3.org/TR/html4/interact/forms.html#h-17.4
        on ne retiendra que l'essentiel....!
        """
        
        self.style       = popKey(kw, 'style'       )
        self.name        = popKey(kw, 'name'        )
        self.id          = popKey(kw, 'id', self.name)
        self.type        = popKey(kw, 'type', 'text')
        self.value       = popKey(kw, 'value'       )
        self.checked     = popKey(kw, 'checked'     )
        self.disabled    = popKey(kw, 'disabled'    )
        self.readonly    = popKey(kw, 'readonly'    )
        self.maxlength   = popKey(kw, 'maxlength'   )
        self.src         = popKey(kw, 'src'         )
        self.alt         = popKey(kw, 'alt'         )
        self.accesskey   = popKey(kw, 'accesskey'   )
        self.accept      = popKey(kw, 'accept'      )
        self.onclick     = popKey(kw, 'onclick'     )
        self._label      = popKey(kw, 'label', ' ' )
        
       
    def __str__(self):
        input = '<input '
        for key in self.__dict__:
            if self.__dict__[key] and not key.startswith('_'):
                input += " "+key+"='"+str(self.__dict__[key])+"'"
        return input+' />'
 
class TextArea(main):
    """ http://www.w3.org/TR/html4/interact/forms.html#h-17.7
    """
    def __init__(self, **kw):  
        self.id          = popKey(kw, 'id'          )
        self.class_style = popKey(kw, 'class_style' )
        self.style       = popKey(kw, 'style'       )
        self.name        = popKey(kw, 'name'        )
        self.rows        = popKey(kw, 'rows'        )
        self.cols        = popKey(kw, 'cols'        )
        self.disabled    = popKey(kw, 'disabled'    )
        self.readonly    = popKey(kw, 'readonly'    )
        self.tabindex    = popKey(kw, 'tabindex'    )
        self.accesskey   = popKey(kw, 'accesskey'   )
        
        
        self._content     = popKey(kw, 'content', '')
        self._label       = popKey(kw, 'label', ' ' )
           
    def __str__(self):
        S = '<textarea '
        for key in self.__dict__:
            if self.__dict__[key] and not key.startswith('_'):
                S += " "+key+"='"+str(self.__dict__[key])+"'"
        S +=  '>'
        S +=  str(self._content)  
        return S+'</textarea><p class="style_cliquable" onclick="selected_textarea=this.previousSibling;javascript:get(\'/get/file\', \'file_area\')" >Inserer un fichier</p>'   
 


class Select(main):
    def __init__(self, items, **kw):
        self.id          = popKey(kw, 'id'          )
        self.class_style = popKey(kw, 'class_style' )
        self.style       = popKey(kw, 'style'       )
        self.name        = popKey(kw, 'name'        )
        self.size        = popKey(kw, 'size'        )
        self.multiple    = popKey(kw, 'multiple'    )
        self.disabled    = popKey(kw, 'disabled'    )
        self.tabindex    = popKey(kw, 'tabindex'    )
        self._items      = items
        self._label      = popKey(kw, 'label', ' '   )
        
    
    def __str__(self):
        S = '<select '
        for key in self.__dict__:
            if self.__dict__[key] and type(self.__dict__[key]) is str:
                S += " "+key+"='"+str(self.__dict__[key])+"'"
        S += '>\n <option> </option>\n'
        
       
        for i in self._items:
            S += '\r'+str(i)
           
        
        for i in range(OptGroup.cpt):
            S += '</optgroup>\n'
        OptGroup.cpt = 0
        return S + '</select>'
    


class Option(object):
    def __init__(self, **kw):
        self.id          = popKey(kw, 'id'          )
        self.class_style = popKey(kw, 'class_style' )
        self.style       = popKey(kw, 'style'       )
        self.name        = popKey(kw, 'name', ' '   )
        self.size        = popKey(kw, 'size'        )
        self.multiple    = popKey(kw, 'multiple'    )
        self.disabled    = popKey(kw, 'disabled'    )
        self.tabindex    = popKey(kw, 'tabindex'    )
        
        self._label      = popKey(kw, 'label', self.name   )
        
    def __str__(self):
        S = '<option '
        for key in self.__dict__:
            if self.__dict__[key] and not key.startswith('_'):
                S += " "+key+"='"+str(self.__dict__[key])+"'"
        S += '>'+self._label+'</option>\n'
        return S
             
       
class OptGroup:
    cpt = 0
    def __init__(self, **kw):
        self.id          = popKey(kw, 'id'          )
        self.class_style = popKey(kw, 'class_style' )
        self.style       = popKey(kw, 'style'       )
        self.name        = popKey(kw, 'name', ' '   )
        self.size        = popKey(kw, 'size'        )
        self.multiple    = popKey(kw, 'multiple'    )
        self.disabled    = popKey(kw, 'disabled'    )
        self.tabindex    = popKey(kw, 'tabindex'    )
        self.label       = popKey(kw, 'label', self.name)
        
    def __str__(self):
        self.__class__.cpt += 1
        S = ''
        if self.__class__.cpt > 1:
           S += '</optgroup>\n' 
           self.__class__.cpt -=1
        S += '<optgroup '
        for key in self.__dict__:
            if self.__dict__[key]  and not key.startswith('_'):
                S += " "+key+"='"+str(self.__dict__[key])+"'"
        S += '>\n'
        return S
      
   
     



class Forms:
    def __init__(self, **kw):
        self.action      = popKey(kw, 'action'          )
        self.method      = popKey(kw, 'method', 'post'  )
        self.id          = popKey(kw, 'id'              )
        self.onsubmit    = popKey(kw, 'onsubmit', 'javascript:return(false)')
  
    def __setattr__(self, name, value):
#         print name, value
        self.__dict__[name] = value
    

    def constraint(self, environ):
        pass    
        
        
        
   
    def __call__(self, environ , **kw):
        #option de mise en forme du formulaire
        # un fieldset avec un label peut etre mis autour du formulaire 
        fieldset    = popKey(kw, 'fieldset', False)
        label       = popKey(kw, 'label', '')
        
        #Champ sous forme de liste
        dfn         = popKey(kw, 'dfn', True)
   
        fieldstorage = environ.get('wsgi.post_form')
        if fieldstorage:
            form = fieldstorage[2]
      
        #on autorise la redefinition de id et action lors d'un appel
        # en effet pourquoi s'en priver ? 
        self.id     = popKey(kw, 'id', self.id)
        self.action = popKey(kw, 'action', self.action)
                 
        def start_form():
            """Permet de demarrer un formulaire
            """
            S = '<div class="file_area" id="file_area"></div><form '
            for key in self.__dict__:
                if self.__dict__[key]:
                    S += key+"='"+str(self.__dict__[key])+"'  "
            S += '>\n'
            if fieldset:
                S += '\n<fieldset>\n'
                #in label que si fieldset
                if label:    
                    S += '<legend>'+ str(label) +'</legend>'
            if dfn:
                S += '\n<dl>'
                      
            
            return S
                
        def end_form():
            """Termine un formulaire
            """
            S = ""
            if dfn:
                S += '\n</dl>'
            if fieldset:
                S += '\n</fieldset>'
            S += '\n</form>'
            return S
                  
        # pb d'ordre des dicos resolu par une liste facultative dans
        # la sous-classe, sinon dans l'ordre du dico (aleatoire)
        S = start_form()
        if self.__class__.__dict__.has_key('enum'):
            for i in self.__class__.enum:
                if fieldstorage and i.type !='password':
                        i.value = form.getfirst(str(i.name))
                if dfn:
                    S += i.set_label()
                else:
                    S +=  str(i)
                S += '<br />'
        else:
            for (name, element) in vars(self.__class__).iteritems():
                if not '__' in name:
                    if dfn:
                        S += element.set_label()
                    else:
                        S += str(element)
                S += '<br />'       
        return S + end_form()





def formsAuto():
    import model
    from sqlobject import SQLObject
    try:
        fd = open('formulaire.py', 'w')
    except IOError:
        print "Impossible d'ouvrir forms.py - pas de generation de formulaire automatique"
    fd.write("from pyson.pylib.forms import *\n")

    for (name, table) in vars(model).iteritems():
        if (inspect.isclass(table)) and (issubclass(table, SQLObject)) & (table != SQLObject):
            if not name.startswith('Assigned'):
                S = '\nclass '+name+'(Forms):\n'
                enum = ""
                code =  inspect.getsourcelines(table)[0]
                for key in map(lambda x: x.strip(), map(lambda x: x.split('=')[0], code)):
                    if not table.__dict__.get(key):
                        continue
                    length = taille(key, code)
                    if length:
                        balise = 'TextArea'
                    else:
                        balise = 'Input'
                        length = "100"
                    if type(table.__dict__[key]) is property and not key.startswith('_'):
                        S += '    '+key+' = '+balise+'(name="'+key+'", maxlength='+length+', label="'+key+'")\n'
                        enum += key+','         
                S += '    submit = Input(type="submit", value="valider",  name="valider", onclick="")\n'
                S += '    enum=['+enum+' submit]\n\n'
                fd.write(S)
    fd.close()
    print "Formulaire genere avec succes\nCreation du fichier formulaire.py editable pour gerer les contraintes" 



def taille(key, code):
    for i in code:
        line = i.strip()
        if line.startswith(key):
            length = re.search('length=(\d+)', line)
            if length:
                if int(length.group(1)) > 100:
                    return length.group(1)
    return False            


def null(environ, field):
     return not environ['POST_'+field.upper()]

def length_gt(environ, field, length=100):
    return len(environ['POST_'+field.upper()]) > length


class Login(Forms):
    pseudo      = Input(name='login', label='Pseudo', maxlength=100, constraint="")
    password    = Input(name='pwd', type='password', label='Mot de passe')
    valider     = Input(type='submit', value='valider',  name="valider" )
    enum = [pseudo, password, valider]
    def constraint(self, environ):
        if null(environ, 'login'):
            return 'Le champ login doit etre rempli'
        if null(environ, 'pwd'):
            return 'le champ password doit etre rempli'


from formulaire import *
