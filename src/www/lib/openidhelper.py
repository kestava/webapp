from pprint import pprint, pformat

import cherrypy
from openid.consumer.consumer import Consumer
from openid.store.filestore import FileOpenIDStore

from lib.applicationpaths import ApplicationPaths
from model.database import grab_connection

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
        
        if 'success' == response.status:
            print('Identity URL: {0}'.format(response.identity_url))
            cls.__on_successful_login()
            
        elif 'cancel' == response.status:
            raise cherrypy.HTTPRedirect('/error/openid?reason=cancelled')
            
        else:
            print('{0} {1}'.format(response.status, response.message))
            raise cherrypy.HTTPRedirect('/error/openid')
            
    @classmethod
    def __on_successful_login(cls):
        cls.__check_account()
        postLoginUrl = cherrypy.session.get('post-login-url')
        if not postLoginUrl is None:
            raise cherrypy.HTTPRedirect(postLoginUrl)
        raise cherrypy.HTTPRedirect('/')
        
    @classmethod
    def __check_account(cls):
        #pool = cherrypy.thread_data.db_connection_pool
        #conn = pool.getconn()
        
        with grab_connection() as conn:
            pass