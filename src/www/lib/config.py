import cherrypy

class Config(object):

    @classmethod
    def get_environment(cls):
    
        if 'environment' in cherrypy.config:
            return cherrypy.config['environment']
            
        return 'development'
        