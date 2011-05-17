
from pprint import pprint, pformat

import cherrypy

class SessionHelper(object):

    def clear_user_data(self):
        a = cherrypy.session.keys()
        for i in a:
            if i.startswith('user.'):
                del cherrypy.session[i]
                
    def push(self, name, value):
        cherrypy.session[name] = value
        
    def pop(self, name):
        val = cherrypy.session.get(name)
        del cherrypy.session[name]
        return val
    
    def has_key(self, name):
        return name in cherrypy.session.keys()
        
    @property
    def userAccountId(self):
        return cherrypy.session.get('user.account_id')
        
    @userAccountId.setter
    def userAccountId(self, value):
        cherrypy.session['user.account_id'] = value
    
    @property
    def postLoginReturnToPath(self):
        return cherrypy.session.get('user.post_login_return_to')
        
    @postLoginReturnToPath.setter
    def postLoginReturnToPath(self, value):
        cherrypy.session['user.post_login_return_to'] = value
        
    @postLoginReturnToPath.deleter
    def postLoginReturnToPath(self):
        del cherrypy.session['user.post_login_return_to']