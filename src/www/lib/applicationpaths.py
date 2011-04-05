"""
This is the **applicationpaths** module.
"""

import urlparse

import cherrypy

from lib.config import Config

class ApplicationPaths(object):
    """This is the **ApplicationPaths** class."""
    
    class PathsDescr(object):
        def __get__(self, instance, owner):
            return {}
    
    paths = PathsDescr()
    
    @classmethod
    def get_script_path(cls, filespec):
        """
        Returns an absolute path relative to the script file.
        """
        if filespec['dynamic']:
            return '/dynamic/js/' + filespec['filename']
        
        return '/js/' + filespec['filename']
    
    @classmethod
    def get_site_root(cls):
        config = cherrypy.request.app.config
        portString = ''
        if 'sitePort' in config['appSettings'] and not 80 == config['appSettings']['sitePort']:
            portString = ':{0}'.format(config['appSettings']['sitePort'])
            
        return 'http://{0}{1}/'.format(config['appSettings']['siteHostname'], portString)
    
    @classmethod
    def get_handle_openid_auth_response_path(cls):
        return urlparse.urljoin(cls.get_site_root(), 'login/openid/process')