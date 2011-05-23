
from modelobjectbase import ModelObjectBase

class AuthenticationProviders(ModelObjectBase):
    
    key = 'authenticationProviders'
    
    def read(self):
        o = [
            {
                'type': 'openid',
                'id': 'google',
                'text': 'Google'
            },
            {
                'type': 'openid',
                'id': 'yahoo',
                'text': 'Yahoo!'
            },
            {
                'type': 'oath',
                'id': 'twitter',
                'text': 'Twitter'
            }
        ]
        
        return o
        