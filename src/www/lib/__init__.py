"""
.. automodule:: lib.applicationpaths
.. automodule:: lib.openidhelper
.. automodule:: lib.sessionhelper
.. automodule:: lib.settingshelper
.. automodule:: lib.useragentinfo
"""

from pprint import pformat

import cherrypy

from model.uniquerequest import UniqueRequest

def make_netloc(ssl=False):
    c = cherrypy.request.app.config
    hostname = c['appSettings']['siteHostname']
    if ssl:
        port = c['appSettings']['external_socket_port_ssl']
        portString = '' if port == 443 else ':{0}'.format(port)
    else:
        port = c['appSettings']['external_socket_port']
        portString = '' if port == 80 else ':{0}'.format(port)
        
    return '{0}{1}'.format(hostname, portString)
