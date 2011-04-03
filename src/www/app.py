import os.path
import pprint
import logging
from logging.handlers import TimedRotatingFileHandler

import cherrypy

# tools
import tools.connectdb
import tools.requestdebugging

import settings
import mapping.rootpages

def configure():

    sourceDirectory = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    staticDirectoryRoot = os.path.join(sourceDirectory, 'static')
    
    serverConfig = {
        'appSettings': {},
        'global': {},
        '/': {
            'tools.gzip.on': True,
            'tools.gzip.mime_types': ['text/html', 'text/css', 'text/plain', 'application/javascript'],
            'tools.sessions.on': True,
            'tools.sessions.name': settings.config['session_cookie_name'],
            'tools.sessions.storage_type': 'file',
            'tools.sessions.storage_path': settings.config['session_storage_path'],
            'tools.sessions.timeout': settings.config['session_timeout'],
            'tools.staticdir.root': staticDirectoryRoot,
            'tools.disconnect_db.on': True,
            'tools.trailing_slash.on': False
        }
    }
    
    # Apply certain settings optionally or accept the default
    if 'socket_host' in settings.config:
        serverConfig['global']['server.socket_host'] = settings.config['socket_host']
        
    if 'socket_port' in settings.config:
        serverConfig['global']['server.socket_port'] = settings.config['socket_port']
    
    serverConfig['appSettings'].update(settings.config['appSettings'])
    
    if 'environment' in settings.config:
        cherrypy.config.update({ 'environment': settings.config['environment'] })
    
    return serverConfig
    
def setup_logging():
    '''Set up a TimedRotatingFileHandler'''
    log = cherrypy.log
    
    # Remove the default FileHandlers if present.
    log.error_file = ""
    log.access_file = ""

    h = TimedRotatingFileHandler(
        filename=settings.config['error_log_path'],
        when=settings.config['error_log_when'],
        interval=settings.config['error_log_interval'],
        backupCount=settings.config['error_log_backups'])
    
    h.setLevel(logging.DEBUG)
    h.setFormatter(cherrypy._cplogging.logfmt)
    log.error_log.addHandler(h)
    
    h = TimedRotatingFileHandler(
        filename=settings.config['access_log_path'],
        when=settings.config['access_log_when'],
        interval=settings.config['access_log_interval'],
        backupCount=settings.config['access_log_backups'])
    
    h.setLevel(logging.DEBUG)
    h.setFormatter(cherrypy._cplogging.logfmt)
    log.access_log.addHandler(h)
    
def main():
    setup_logging()
    
    cherrypy.quickstart(
        root=mapping.rootpages.RootPages(),
        config=configure()
    )
    
if __name__ == '__main__':
    main()