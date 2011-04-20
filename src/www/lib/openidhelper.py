from pprint import pprint, pformat

import cherrypy
from openid.consumer.consumer import Consumer
from openid.store.filestore import FileOpenIDStore

from lib.applicationpaths import ApplicationPaths
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
        
        if 'success' == response.status:
            print('Identity URL: {0}'.format(response.identity_url))
            cls.__on_success(response.identity_url)
            
        elif 'cancel' == response.status:
            raise cherrypy.HTTPRedirect('/error/openid?reason=cancelled')
            
        else:
            print('{0} {1}'.format(response.status, response.message))
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
        by providing some very basic information (e.g. first and last name,
        e-mail).
        """
        
        accountId = OpenIdAccount.get_account_id(identity_url)
        if not accountId is None:
            cherrypy.session['user.account_id'] = accountId
            postLoginUrl = cherrypy.session.get('user.post_login_url')
            if not postLoginUrl is None:
                raise cherrypy.HTTPRedirect(postLoginUrl)
            raise cherrypy.HTTPRedirect('/')
        else:
            raise cherrypy.HTTPRedirect('/accounts/create')
        