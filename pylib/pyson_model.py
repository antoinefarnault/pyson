from sqlobject import *
from datetime import datetime
"""
    Description des tables de la base de donnees

    NB : l attribut id est cree par defaut
    """

"Table Users"
class Users(SQLObject):
    nom         = StringCol(length=100)
    prenom      = StringCol(length=100)
    pseudo      = StringCol(length=100, unique=True)
    password    = StringCol(length=100)
    _groupes    = RelatedJoin('Groupe', intermediateTable='assigned_groupes', createRelatedTable=False)

"Table Groupe"
class Groupe(SQLObject):
    nom         = StringCol(length=100, unique=True)
    _roles      = RelatedJoin('Role',intermediateTable='assigned_roles', createRelatedTable=False)
    _users      = RelatedJoin('Users', intermediateTable='assigned_groupes', createRelatedTable=False)

"Table Role"
class Role(SQLObject):
    name       = StringCol(length=20, unique=True)
    _groupes     = RelatedJoin('Groupe', intermediateTable='assigned_roles', createRelatedTable=False)

""
class AssignedGroupes(SQLObject):
    class sqlmeta:
        table = 'assigned_groupes'
    users = ForeignKey('Users', notNull=True, cascade=True)
    groupe = ForeignKey('Groupe', notNull=True, cascade=True)
    _unique = index.DatabaseIndex(users, groupe, unique=True)
 
class AssignedRoles(SQLObject):
    class sqlmeta:
        table = 'assigned_roles'
    groupe = ForeignKey('Groupe', notNull=True, cascade=True)
    role = ForeignKey('Role', notNull=True, cascade=True)
    _unique = index.DatabaseIndex(role, groupe, unique=True)
           
           
         


def getKeyDict(_class):
    dict = {}
    for key in _class.__dict__:
        if type(_class.__dict__[key]) is property and not key.startswith('_'):
    
            dict[key] = key
    return dict
