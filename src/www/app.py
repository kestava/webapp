import os.path
import pprint

import cherrypy

import settings
import mapping.rootpages

def configure():

    sourceDirectory = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    staticDirectoryRoot = os.path.join(sourceDirectory, 'static')
    
    serverConfig = {
        'global': {
            'server.socket_host': settings.config['socket_host'],
            'server.socket_port': settings.config['socket_port'],
            'log.screen': False,
            'log.access_file': settings.config['access_log_path'],
            'log.error_file': settings.config['error_log_path']
        },
        '/': {
            'tools.gzip.on': True,
            'tools.gzip.mime_types': ['text/html', 'text/css', 'text/plain', 'application/javascript'],
            'tools.sessions.on': True,
            'tools.sessions.name': 'KESTAVA_SESSION_COOKIE',
            'tools.sessions.storage_type': 'file',
            'tools.sessions.storage_path': settings.config['session_storage_path'],
            'tools.staticdir.root': staticDirectoryRoot,
            'tools.trailing_slash.missing': False
        },
        '/css': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'css'
        },
        '/js': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'js'
        },
        '/img': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'img'
        }
    }
    
    # Add a "development" environment
    cherrypy._cpconfig.environments['development'] = {
        'engine.autoreload_on': True,
        'checker.on': True,
        'tools.log_headers.on': True,
        'request.show_tracebacks': True,
        'log.screen': False
    }
    
    # available default environments: "staging", "production", "embedded",
    # "test_suite" (see _cpconfig.environments dict for their predefined
    # settings).  To these, we've added "development".
    cherrypy.config.update({ 'environment': settings.config['environment'] })
    
    return serverConfig

def main():
    cherrypy.quickstart(
        root=mapping.rootpages.RootPages(),
        config=configure()
    )
    
if __name__ == '__main__':
    main()