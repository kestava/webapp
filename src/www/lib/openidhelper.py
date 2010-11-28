import pprint

import cherrypy
from openid.consumer.consumer import Consumer
from openid.store.filestore import FileOpenIDStore
from openid.extensions.sreg import SRegRequest, SRegResponse
from openid.extensions.ax import FetchRequest, FetchResponse, AttrInfo

from lib.applicationpaths import ApplicationPaths
from model.openidaccount import OpenIdAccount
from model.account import Account

class OpenIdHelper(object):
    
    @classmethod
    def get_auth_redirect_url(cls, identifier):
        s = FileOpenIDStore(cherrypy.request.app.config['appSettings']['openIdDataStoreDirectory'])
        consumer = Consumer(session=cherrypy.session, store=s)
        #consumer.setAssociationPreference([('HMAC-SHA256', 'DH-SHA256')])
        authRequest = consumer.begin(identifier)
        
        # sreg
        authRequest.addExtension(SRegRequest(required=['email'], optional=['fullname']))
        
        # ax
        axFetchRequest = FetchRequest()
        axFetchRequest.add(AttrInfo(type_uri='http://axschema.org/contact/email', required=True))
        axFetchRequest.add(AttrInfo(type_uri='http://axschema.org/namePerson', required=True))
        axFetchRequest.add(AttrInfo(type_uri='http://axschema.org/namePerson/first', required=True))
        axFetchRequest.add(AttrInfo(type_uri='http://axschema.org/namePerson/last', required=True))
        authRequest.addExtension(axFetchRequest)
        
        return authRequest.redirectURL(
            realm=ApplicationPaths.get_site_root(),
            return_to=ApplicationPaths.get_handle_openid_auth_response_path())
        
    @classmethod
    def handle_auth_response(cls, query):
        #pprint.pprint(query)
        
        s = FileOpenIDStore(cherrypy.request.app.config['appSettings']['openIdDataStoreDirectory'])
        consumer = Consumer(session=cherrypy.session, store=s)
        response = consumer.complete(
            query=query,
            current_url=ApplicationPaths.get_handle_openid_auth_response_path())
        
        if 'success' == response.status:
            sregResponse = SRegResponse.fromSuccessResponse(response)
            axResponse = FetchResponse.fromSuccessResponse(response)
            
            email = None
            if sregResponse:
                email = sregResponse.get('email')
            elif axResponse:
                email = axResponse.data['http://axschema.org/contact/email'][0]
            
            if not OpenIdAccount.exists(identifier=response.identity_url):
                # start a transaction to enclose creation of the OpenID account
                # record and any other database records that need to be created
                # at the same time                
                OpenIdAccount.create(identifier=response.identity_url, email=email)
                
            cherrypy.session['account-id'] = Account.get_account_id_by_email(email)
            
            raise cherrypy.HTTPRedirect(cls.__get_return_to_path())
        elif 'cancel' == response.status:
            raise cherrypy.HTTPRedirect('/error/openid?reason=cancelled')
        else:
            print('{0} {1}'.format(response.status, response.message))
            raise cherrypy.HTTPRedirect('/error/openid')
            
    @classmethod
    def __get_return_to_path(cls):
        o = '/'
        
        if cherrypy.session.has_key('return-to-after-login'):
            o = cherrypy.session.get('return-to-after-login')
        
        return o
            