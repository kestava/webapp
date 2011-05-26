
import cherrypy

from modelobjectbase import ModelObjectBase
from model import grab_connection, get_row
from lib.sessionhelper import SessionHelper

class UserData(ModelObjectBase):
    
    key = 'userData'
    
    def read(self):
        o = {}
        userAccountId = SessionHelper().peek('user.account_id')
        if not userAccountId is None:
            
            with grab_connection('main') as conn:
                data = get_row(
                    conn,
                    """
                    select user_name, first_name, last_name, email
                    from user_accounts where user_account_id = %(i)s
                    """,
                    { 'i': userAccountId })
            
            if data:
                o['userAccountId'] = userAccountId
                o['userName'] = data['user_name']
                o['firstName'] = data['first_name']
                o['lastName'] = data['last_name']
                o['email'] = data['email']
                
        return o
        