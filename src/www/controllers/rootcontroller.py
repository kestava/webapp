# _*_ coding: utf-8 _*_

from pprint import pprint, pformat

import cherrypy

from accountcontroller import AccountController
from analysiscontroller import AnalysisController
from conversationscontroller import ConversationsController
from dynamicfilescontroller import DynamicFilesController
from errorcontroller import ErrorController
from marketdatacontroller import MarketDataController
from postcontroller import PostController
from searchcontroller import SearchController
from transactionscontroller import TransactionsController

from model.userdatatheme import UserDataTheme
from model.userdata import UserData
from model.sitedata import SiteData

class RootController(object):

    account = AccountController()
    analysis = AnalysisController()
    conversations = ConversationsController()
    dynamic = DynamicFilesController()
    error = ErrorController()
    marketdata = MarketDataController()
    post = PostController()
    search = SearchController()
    transactions = TransactionsController()

    @cherrypy.tools.build_model(classes=[
        UserData,
        UserDataTheme,
        SiteData])
    @cherrypy.expose
    def index(self):
        r = cherrypy.request
        env = r.app.jinjaEnv
        template = env.get_template('html/{0}/homepage'.format(r.model['userData']['themeName']))
        return template.render(model=r.model)
    
    @cherrypy.tools.build_model(classes=[SiteData])
    @cherrypy.expose(alias='xrds.xml')
    def handle_xrds(self):
        # TODO: Create a tool to add the following response header pointing to
        # this document:
        # cherrypy.response.headers['X-XRDS-Location']
        req = cherrypy.request
        cherrypy.response.headers['content-type'] = 'application/xrds+xml'
        template = req.app.jinjaEnv.get_template('html/misc/xrds')
        return template.render(model=req.model)