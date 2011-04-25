import argparse
from pprint import pprint, pformat

import cherrypy
import psycopg2.pool

# tools
import tools.buildmodel
import tools.detectuseragent
import tools.sitemoderedirector
import tools.sitemode
    
from controllers.rootcontroller import RootController
from plugins.setupjinjaenvironment import SetupJinjaEnvironment
from plugins.setuppgconnectionpool import SetupPgConnectionPool
from plugins.setprocesstitle import SetProcessTitle
from plugins.setlogging import SetLogging


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
    
def main(config):

    SetLogging().subscribe()
    SetProcessTitle().subscribe()
    SetupJinjaEnvironment().subscribe()
    SetupPgConnectionPool(
        pool_name='main',
        db_name=config['appSettings']['main_db.name'],
        db_user=config['appSettings']['main_db.role']).subscribe()
    
    cherrypy.quickstart(
        root=RootController(),
        config=config)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='The main Kestava web application')
    parser.add_argument('-c', '--config',
        dest='config_file', help='The full path to the configuration file for this instance.',
        required=True)
    args = parser.parse_args()
    config = get_config(args.config_file)
    main(config)
