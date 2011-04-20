import argparse
from pprint import pprint, pformat
from ConfigParser import ConfigParser
import site
import sys
import os

import cherrypy
import psycopg2.pool

# tools
import tools.buildmodel
    
from controllers.rootcontroller import RootController
from plugins.setupjinjaenvironment import SetupJinjaEnvironment
from plugins.setuppgconnectionpool import SetupPgConnectionPool
from plugins.setprocesstitle import SetProcessTitle
from plugins.setlogging import SetLogging

def add_wurfl_path(config_path):
    """
    Update the Python search path using the appSettings.wurfl.include_path setting
    """
    parser = ConfigParser()
    parser.read(config_path)
    if parser.has_option('appSettings', 'wurfl.include_path'):
        wurflPath = parser.get('appSettings', 'wurfl.include_path').strip('\'"')
        if not os.path.exists(wurflPath):
            raise Exception('Invalid WURFL include path')
        site.addsitedir(wurflPath)
    else:
        raise Exception('Configuration must specify the wurfl.include_path option')
        
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
    
    # environment configuration
    add_wurfl_path(args.config_file)
    import tools.detectuseragent

    main(config_file_path=args.config_file)
