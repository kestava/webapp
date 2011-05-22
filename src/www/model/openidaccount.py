
from pprint import pformat

from model import grab_connection, get_scalar, execute_action

class OpenIdAccount(object):
    
    def get_account_id(self, identity_url):
        with grab_connection('main') as conn:
            return get_scalar(
                conn,
                'select ref_user_account_id from openid_accounts where openid_identifier = %(i)s',
                { 'i': identity_url },
                'ref_user_account_id')
            
    def create(self, connection, userAccountId, oidIdentifier):
        execute_action(
            connection,
            """
            insert into openid_accounts (ref_user_account_id, openid_identifier)
            values (%(i)s, %(o)s)
            """,
            { 'i': userAccountId, 'o': oidIdentifier})
        