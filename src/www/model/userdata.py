
import cherrypy

from modelobjectbase import ModelObjectBase
from model import grab_connection, get_row

class UserData(ModelObjectBase):
    
    key = 'userData'
    
    def read(self):
        o = {}
        
        o['accountId'] = cherrypy.session.get('user.account_id')
        if not o['accountId'] is None:
            
            with grab_connection('main') as conn:
                data = get_row(
                    conn,
                    """
                    select user_name, first_name, last_name, email
                    from user_accounts where user_account_id = %(i)s
                    """,
                    { 'i': o['accountId'] })
            
            o['userName'] = data['user_name']
            o['firstName'] = data['first_name']
            o['lastName'] = data['last_name']
            o['email'] = data['email']
                
        return o
        