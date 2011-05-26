
from model import get_scalar_nc, execute_action

class UserAccount(object):
    
    def create(self, connection, params):
        row = execute_action(
            connection,
            """
            insert into user_accounts (first_name, user_name, email)
            values (%(f)s, %(u)s, %(e)s) returning user_account_id
            """,
            {
                'f': params['first_name'],
                'u': params['user_name'],
                'e': params['email']
            },
            True
        )
        
        id = row['user_account_id']
        
        if 0 < len(params['last_name']):
            execute_action(
                connection,
                """
                update user_accounts set last_name = %(l)s
                where user_account_id = %(i)s
                """,
                { 'l': params['last_name'], 'i': id }
            )
            
        return id
        
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
        
    def username_in_use(self, username):
        return get_scalar_nc(
            'main',
            """
            select exists (select 0 from user_accounts
            where user_name like %(u)s) as e
            """,
            { 'u': username },
            'e')
        