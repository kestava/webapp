
from pprint import pformat

from psycopg2.extras import DictCursor

from model.database import grab_connection

class OpenIdAccount(object):
    
    @classmethod
    def get_user_id(cls, identity_url):
        with grab_connection('main') as conn:
            cur = conn.cursor(cursor_factory=DictCursor)
            cur.execute(
                'select account_id from openid_accounts where openid_identifier = %(i)s',
                { 'i': identity_url })
            
            data = cur.fetchone()
            if not data is None:
                return data['account_id']