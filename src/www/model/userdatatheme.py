
import cherrypy

from modelobjectbase import ModelObjectBase

class UserDataTheme(ModelObjectBase):
    
    key = 'userData'
    
    def read(self):
        return {
            'themeName': 'default',
            'accountId': cherrypy.session.get('user-account-id')
        }
        
    