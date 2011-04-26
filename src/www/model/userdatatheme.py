
import cherrypy

from modelobjectbase import ModelObjectBase

class UserDataTheme(ModelObjectBase):
    
    key = 'userData'
    
    def read(self):
        o = {}
        
        o['themeName'] = 'default'
        o['jQueryUiTheme'] = 'ui-lightness'
        o['accountId'] = cherrypy.session.get('user.account_id')
        
        return o
        
    