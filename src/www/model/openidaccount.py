import pprint

import cherrypy

from database import with_cursor
from account import Account

class OpenIdAccount(object):
    
    @classmethod
    def exists(cls, identifier):
        def _exists(cursor):
            cursor.execute(
                'select openid_identifier, account_id from openid_accounts where openid_identifier = %(url)s',
                { 'url': identifier })
            row = cursor.fetchone()
            _exists.result = not row is None
            
        with_cursor(func=_exists)
        
        return _exists.result
        
    @classmethod
    def create(cls, identifier, email):
        
        def _create(cursor):
            accountId = Account.get_account_id_by_email(email, cursor=cursor)
            if not accountId:
                accountId = Account.create(email=email, cursor=cursor)
            
            cursor.execute(
                '''insert into openid_accounts (openid_identifier, account_id) \
values (%(oid)s, %(aid)s)''',
                {
                    'oid': identifier,
                    'aid': accountId
                })
            
        with_cursor(_create)
        