"""
This is the **config** module.
"""

import cherrypy

class Config(object):
    """
    This is the **Config** class.
    """
    
    @classmethod
    def get_environment(cls):
    
        if 'environment' in cherrypy.config:
            return cherrypy.config['environment']
            
        return 'development'
        