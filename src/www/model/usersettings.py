
import cherrypy

from modelobjectbase import ModelObjectBase

class UserSettings(ModelObjectBase):
    
    key = 'userSettings'
    
    def read(self):
        o = {}
        
        o['layout'] = 'default'
        o['jQueryUiTheme'] = 'ui-lightness'
        
        return o
        
    