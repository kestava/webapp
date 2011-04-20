
from pprint import pprint, pformat

import cherrypy

class SessionHelper(object):

    def clear_user_data(self):
        a = cherrypy.session.keys()
        for i in a:
            if i.startswith('user.'):
                del cherrypy.session[i]