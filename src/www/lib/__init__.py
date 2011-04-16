"""
.. automodule:: lib.sessiondata
.. automodule:: lib.sitedata
"""

from pprint import pformat

import cherrypy

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