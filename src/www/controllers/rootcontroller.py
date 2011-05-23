# _*_ coding: utf-8 _*_
"""
.. autoclass:: RootController
    :members: index, set_site_mode, credits
"""

from pprint import pprint, pformat

import cherrypy

from account.accountcontroller import AccountController
from analysiscontroller import AnalysisController
from conversationscontroller import ConversationsController
from dynamicfilescontroller import DynamicFilesController
from errorcontroller import ErrorController
from marketdatacontroller import MarketDataController
from postcontroller import PostController
from searchcontroller import SearchController
from transactionscontroller import TransactionsController
from mobilecontroller import MobileController

from model.viewdata.usersettings import UserSettings
from model.viewdata.userdata import UserData
from model.viewdata.sitedata import SiteData
from model.viewdata.credits import Credits

class RootController(object):

    account = AccountController()
    analysis = AnalysisController()
    conversations = ConversationsController()
    dynamic = DynamicFilesController()
    error = ErrorController()
    marketdata = MarketDataController()
    mobile = MobileController()
    post = PostController()
    search = SearchController()
    transactions = TransactionsController()

    @cherrypy.tools.build_model(includes=[
        UserData(),
        UserSettings(),
        SiteData()])
    @cherrypy.expose
    def index(self):
        r = cherrypy.request
        env = r.app.jinjaEnv
        template = env.get_template('html/{0}/homepage.html'.format(r.model['userSettings']['layout']))
        return template.render(model=r.model)
    
    @cherrypy.tools.build_model(includes=[SiteData()])
    @cherrypy.expose(alias='xrds.xml')
    def handle_xrds(self):
        # TODO: Create a tool to add the following response header pointing to
        # this document:
        # cherrypy.response.headers['X-XRDS-Location']
        req = cherrypy.request
        cherrypy.response.headers['content-type'] = 'application/xrds+xml'
        template = req.app.jinjaEnv.get_template('html/misc/xrds.xml')
        return template.render(model=req.model)
        
    @cherrypy.tools.site_mode(mode='any')
    @cherrypy.expose(alias='set-site-mode')
    def set_site_mode(self, edition):
        """
        Some description
        """
        a = {
            'web': '/',
            'mobile': '/mobile'
        }
        b = edition if edition in a else 'web'
        cherrypy.session['user.site_mode'] = b
        
        raise cherrypy.HTTPRedirect(a[b])
        
    @cherrypy.tools.build_model(includes=[
        SiteData(),
        UserData(),
        UserSettings(),
        Credits()])
    @cherrypy.expose
    def credits(self):
        r = cherrypy.request
        env = r.app.jinjaEnv
        template = env.get_template('html/{0}/credits.html'.format(r.model['userSettings']['layout']))
        return template.render(model=r.model)
        