
from pprint import pprint

import cherrypy

from model.uniquerequest import UniqueRequest
from model.openidaccount import OpenIdAccount
from model import grab_connection
from lib.sessionhelper import SessionHelper

class AddController(object):

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
