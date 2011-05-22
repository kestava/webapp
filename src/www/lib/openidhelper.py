from pprint import pprint, pformat

import cherrypy
from openid.consumer.consumer import Consumer
from openid.store.filestore import FileOpenIDStore

from lib.applicationpaths import ApplicationPaths
from lib.sessionhelper import SessionHelper
from model.openidaccount import OpenIdAccount

class OpenIdHelper(object):
    
    @classmethod
    def get_auth_redirect_url(cls, identifier):
        s = FileOpenIDStore(cherrypy.request.app.config['appSettings']['openid.datastore_directory'])
        consumer = Consumer(session=cherrypy.session, store=s)
        authRequest = consumer.begin(identifier)
        return authRequest.redirectURL(
            realm=ApplicationPaths.get_site_root(),
            return_to=ApplicationPaths.get_handle_openid_auth_response_path())
    
    @classmethod
    def handle_auth_response(cls, query):
        settings = cherrypy.request.app.config['appSettings']
        s = FileOpenIDStore(settings['openid.datastore_directory'])
        consumer = Consumer(session=cherrypy.session, store=s)
        response = consumer.complete(
            query=query,
            current_url=ApplicationPaths.get_handle_openid_auth_response_path())
        
        pprint(dir(response))
        print('oid status: {0}'.format(response.status))
        print('oid display identifier: {0}'.format(response.getDisplayIdentifier()))
        print('oid identity_url: {0}'.format(response.identity_url))
        #print('oid message:\n{0}'.format(response.message))
        
        if 'success' == response.status:
            cherrypy.log.error('Identity URL: {0}'.format(response.identity_url))
            cls.__on_success(response.identity_url)
            
        elif 'cancel' == response.status:
            raise cherrypy.HTTPRedirect('/error/openid?reason=cancelled')
            
        else:
            cherrypy.log.error('{0} {1}'.format(response.status, response.message))
            raise cherrypy.HTTPRedirect('/error/openid')
            
    @classmethod
    def __on_success(cls, identity_url):
        """
        The user has successfully authenticated via an OpenID provider.  Now we
        have to determine whether their identity URL is associated with an
        existing site account.  If so, then we route the request to the post-
        login URL, if possible, or to the homepage.  If the identity URL is not
        associated with an existing account, then we route the request to a page
        where we give the user an opportunity to establish a new site account
        by providing some very basic information (e.g. e-mail address).
        """
        s = SessionHelper()
        accountId = OpenIdAccount().get_account_id(identity_url)
        if accountId is None:
            # Publish the OpenID identity url to be used for account creation.
            # The account creation controller will pop it from the session data
            s.push('account_create.openid_identity_url', identity_url)
            raise cherrypy.HTTPRedirect('/account/create')
        else:
            s.push(user.account_id, accountId)
            raise cherrypy.HTTPRedirect('/' if s.has_key('user.post_login_return_to') is None \
                else s.peek('user.post_login_return_to'))
            