
from pprint import pprint

import cherrypy

from model.uniquerequest import UniqueRequest
from model.openidaccount import OpenIdAccount
from model.useraccount import UserAccount

from model.viewdata.userdata import UserData
from model.viewdata.usersettings import UserSettings
from model.viewdata.sitedata import SiteData
from model.viewdata.pagedata import PageData

from model import grab_connection
from lib.sessionhelper import SessionHelper

class AddController(object):

    @cherrypy.tools.build_model(includes=[
        UserData(),
        UserSettings(),
        SiteData(),
        PageData()])
    @cherrypy.expose
    def new(self, sessionKey, request):
        """
        The user has granted permission to create a new account using the e-mail
        address and OpenID identity provided.
        
        Verify their unique request and display a page where they can input
        basic information needed to establish the account
        """
        u = UniqueRequest()
        if not u.exists(sessionKey=sessionKey, requestKey='add_openid.new_account', value=request):
            raise cherrypy.HTTPError(400, 'Invalid request')
        
        r = cherrypy.request
        e = r.app.jinjaEnv
        
        dataParts = u.get_data(sessionKey=sessionKey, requestKey='add_openid.new_account').split('|')
        r.model['pageData']['email'] = dataParts[0]
        r.model['pageData']['oidIdentifier'] = dataParts[1]
        
        return e.get_template(
                'html/{0}/account/add/new.html'.format(
                    r.model['userSettings']['layout']))\
                    .render(model=r.model)
        
        #with grab_connection('main') as conn:
        #    u.delete(connection=conn, sessionKey=sessionKey, requestKey='add_openid.new_account')
        #    id = UserAccount().create(connection=conn, email=email)
        #    OpenIdAccount().create(connection=conn, userAccountId=id, oidIdentifier=oidIdentifier)
        #    SessionHelper().push('user.account_id', id)
        #    
        #raise cherrypy.HTTPRedirect('/')

    @cherrypy.expose
    def email(self, sessionKey, request):
        """
        The user has granted permission to associate the OpenID identifier with
        their existing user account.
        """ 
        # Try to consume the given request
        u = UniqueRequest()
        if not u.exists(sessionKey=sessionKey, requestKey='add_openid.existing_account', value=request):
            raise cherrypy.HTTPError(400, 'Invalid request')
            
        dataParts = u.get_data(sessionKey=sessionKey, requestKey='add_openid.existing_account').split('|')
        id = int(dataParts[0])
        with grab_connection('main') as conn:
            u.delete(connection=conn, sessionKey=sessionKey, requestKey='add_openid.existing_account')
            OpenIdAccount().create(connection=conn, userAccountId=id, oidIdentifier=dataParts[1])
            SessionHelper().push('user.account_id', id)
            
        raise cherrypy.HTTPRedirect('/')
