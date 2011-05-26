
import json

import cherrypy

from model.useraccount import UserAccount

class ServicesController(object):
    
    @cherrypy.expose
    def checkusername(self, username):
        cherrypy.response.headers['content-type'] = 'application/json'
        return json.dumps({
            'username': username,
            'available': not UserAccount().username_in_use(username)
        })
        