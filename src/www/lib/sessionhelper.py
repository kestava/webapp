
from pprint import pprint, pformat

import cherrypy

class SessionHelper(object):

    __all = ['account_create.openid_identity_url',
             'add_openid.existing_account',
             'add_openid.new_account',
             'user.account_id',
             'user.post_login_return_to']

    def clear_user_data(self):
        a = cherrypy.session.keys()
        for i in a:
            if i.startswith('user.'):
                del cherrypy.session[i]
                
    def push(self, name, value):
        self.__validate_name(name)
        cherrypy.session[name] = value
        
    def pop(self, name):
        self.__validate_name(name)
        val = cherrypy.session.get(name)
        del cherrypy.session[name]
        return val
    
    def peek(self, name):
        self.__validate_name(name)
        return cherrypy.session.get(name)
    
    def has_key(self, name):
        self.__validate_name(name)
        return name in cherrypy.session.keys()

    def __validate_name(self, name):
        if not name in self.__all:
            raise cherrypy.HTTPError(500, 'Invalid session variable: {0}'.format(name))
