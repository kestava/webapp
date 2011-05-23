"""
.. autoclass:: ErrorController
    :members: default, openid, login_required
"""

from pprint import pprint, pformat
import logging

import cherrypy

from model.viewdata.sitedata import SiteData
from model.viewdata.usersettings import UserSettings
from model.viewdata.userdata import UserData

class ErrorController(object):

    @cherrypy.expose
    def index(self):
        return 'error (index)'

    @cherrypy.expose
    def default(self, *args, **kwargs):
        cherrypy.log.error(
            'default args: {0}'.format(pformat(args)),
            'ErrorController',
            logging.DEBUG)
        cherrypy.log.error(
            'default kwargs: {0}'.format(pformat(kwargs)),
            'ErrorController',
            logging.DEBUG)
        return 'error (default)'
    
    @cherrypy.expose
    def openid(self):
        return 'error (openid)'
        
    @cherrypy.tools.build_model(includes=[
        SiteData(),
        UserData(),
        UserSettings()])
    @cherrypy.expose(alias='login-required')
    def login_required(self):
        """
        Some description
        """
        r = cherrypy.request
        env = r.app.jinjaEnv
        template = env.get_template('html/{0}/error/loginrequired.html'.format(r.model['userSettings']['layout']))
        return template.render(model=r.model)