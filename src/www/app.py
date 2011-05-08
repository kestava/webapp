import argparse
import logging
from pprint import pprint, pformat

import cherrypy
import psycopg2.pool

# tools
import tools.buildmodel
import tools.detectuseragent
import tools.sitemoderedirector
import tools.sitemode
import tools.requiremethod
import tools.initializedraftpost
    
from controllers.rootcontroller import RootController
from plugins.setupjinjaenvironment import SetupJinjaEnvironment
from plugins.setuppgconnectionpool import SetupPgConnectionPool
from plugins.setprocesstitle import SetProcessTitle

def get_config(config_file_path):

    defaults = {
        '/': {
            'tools.sessions.on': True,
            'tools.sessions.storage_type': 'file',
            'tools.sessions.timeout': 60,
            'tools.trailing_slash.on': False,
            'tools.detect_user_agent.on': True,
            'tools.site_mode_redirector.on': True
        }
    }

    configParser = cherrypy.lib.reprconf.Parser()
    configParser.read(config_file_path)
    config = configParser.as_dict()
    config['/'].update(defaults['/'])
    cherrypy.log.error('Configuration:\n{0}'.format(pformat(config)))
    return config
    
def setup_logging(config):
    log = cherrypy.log
    
    # Remove the default FileHandlers if present
    log.error_file = ''
    log.access_file = ''
    
    errorLogLevel = config['appSettings']['logging.error_log.level']
    log.error_log.setLevel(errorLogLevel)
    
    h = logging.FileHandler(config['appSettings']['logging.error_log.path'])
    h.setFormatter(cherrypy._cplogging.logfmt)
    log.error_log.addHandler(h)
    
    h = logging.FileHandler(config['appSettings']['logging.access_log.path'])
    h.setFormatter(cherrypy._cplogging.logfmt)
    log.access_log.addHandler(h)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='The main Kestava web application')
    parser.add_argument('-c', '--config',
        dest='config_file', help='The full path to the configuration file for this instance.',
        required=True)
    args = parser.parse_args()
    config = get_config(args.config_file)
    setup_logging(config)
    
    # Set plugin subscriptions
    SetProcessTitle().subscribe()
    SetupJinjaEnvironment().subscribe()
    SetupPgConnectionPool(
        pool_name='main',
        db_name=config['appSettings']['main_db.name'],
        db_user=config['appSettings']['main_db.role']).subscribe()
    
    # Reload the application if the configuration file changes
    # Only applies if no 'environment' settings is specified in the
    # configuration file
    cherrypy.engine.autoreload.files.add(args.config_file)
    
    cherrypy.quickstart(
        root=RootController(),
        config=config)
