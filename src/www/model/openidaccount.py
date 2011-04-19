
from pprint import pformat

from model import grab_connection, get_scalar

class OpenIdAccount(object):
    
    @classmethod
    def get_account_id(cls, identity_url):
        with grab_connection('main') as conn:
            return get_scalar(
                conn,
                'select ref_user_account_id from openid_accounts where openid_identifier = %(i)s',
                { 'i': identity_url },
                'ref_user_account_id')
            