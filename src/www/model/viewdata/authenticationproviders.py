
from modelobjectbase import ModelObjectBase

class AuthenticationProviders(ModelObjectBase):
    
    key = 'authenticationProviders'
    
    def read(self):
        o = [
            {
                'type': 'openid',
                'id': 'google',
                'text': 'Google',
                'url': 'https://www.google.com/accounts/o8/id'
            },
            {
                'type': 'openid',
                'id': 'yahoo',
                'text': 'Yahoo!',
                'url': 'http://www.yahoo.com/'
            },
            {
                'type': 'oauth',
                'id': 'twitter',
                'text': 'Twitter'
            },
            {
                'type': 'openid',
                'id': 'myopenid',
                'text': 'myOpenID',
                'url': 'https://www.myopenid.com/'
            }
        ]
        
        return o
        