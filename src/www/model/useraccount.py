
from model import get_scalar_nc

class UserAccount(object):
    
    def id_from_email(self, email):
        return get_scalar_nc(
            'main',
            """
            select a.user_account_id from
            user_accounts as a
            where a.email like %(e)s
            """,
            { 'e': email },
            'user_account_id')