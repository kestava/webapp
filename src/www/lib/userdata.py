
import cherrypy

class UserData(object):
    """Provides data applying to the current user/request"""
    
    __attributes = {
        'themeName': 'get_theme_name'
    }
        
    def __getattr__(self, name):
        
        if not name in self.__attributes:
            raise AttributeError()
            
        return getattr(self, self.__attributes[name])()
        
    def get_theme_name(self):
        o = cherrypy.session.get('user-theme-name')
        return o if not o is None else 'default'