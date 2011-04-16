from pprint import pprint, pformat

import cherrypy
from openid.consumer.consumer import Consumer
from openid.store.filestore import FileOpenIDStore

from lib.applicationpaths import ApplicationPaths

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
        s = FileOpenIDStore(cherrypy.request.app.config['appSettings']['openid.datastore_directory'])
        consumer = Consumer(session=cherrypy.session, store=s)
        response = consumer.complete(
            query=query,
            current_url=ApplicationPaths.get_handle_openid_auth_response_path())
        
        print('OpenID response:\n{0}\n{1}'.format(pformat(response), pformat(dir(response))))
        
        if 'success' == response.status:
            postLoginUrl = cherrypy.session.get('post-login-url')
            if not postLoginUrl is None:
                raise cherrypy.HTTPRedirect(postLoginUrl)
            raise cherrypy.HTTPRedirect(ApplicationPaths.get_site_root())
            
        elif 'cancel' == response.status:
            raise cherrypy.HTTPRedirect('/error/openid?reason=cancelled')
            
        else:
            print('{0} {1}'.format(response.status, response.message))
            raise cherrypy.HTTPRedirect('/error/openid')
            