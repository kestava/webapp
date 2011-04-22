import argparse
from pprint import pprint, pformat

import cherrypy
import psycopg2.pool

# tools
import tools.buildmodel
import tools.detectuseragent
    
from controllers.rootcontroller import RootController
from plugins.setupjinjaenvironment import SetupJinjaEnvironment
from plugins.setuppgconnectionpool import SetupPgConnectionPool
from plugins.setprocesstitle import SetProcessTitle
from plugins.setlogging import SetLogging
        
def main(config_file_path):

    SetLogging().subscribe()
    SetProcessTitle().subscribe()
    SetupJinjaEnvironment().subscribe()
    SetupPgConnectionPool(
        pool_name='main',
        db_name='kestava',
        db_user='kestava').subscribe()

    cherrypy.quickstart(
        root=RootController(),
        config=config_file_path)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='The main Kestava web application')
    parser.add_argument('-c', '--config',
        dest='config_file', help='The full path to the configuration file for this instance.',
        required=True)
    args = parser.parse_args()
    main(config_file_path=args.config_file)
