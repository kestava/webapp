
from model import get_scalar_nc, execute_action

class UserAccount(object):
    
    def create(self, connection, email):
        row = execute_action(
            connection,
            """
            insert into user_accounts (email) values (%(e)s) returning user_account_id
            """,
            { 'e': email },
            True)
        
        return row['user_account_id']
        
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
        