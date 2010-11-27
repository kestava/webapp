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
    def create(cls, identifier, email, firstName, lastName, fullName):
        
        def _create(cursor):
            accountId = Account.get_account_id_by_email(email, cursor=cursor)
            if not accountId:
                accountId = Account.create(email=email, cursor=cursor)
            
            cursor.execute(
                '''insert into openid_accounts (openid_identifier, account_id, \
email, first_name, last_name, full_name) \
values (%(oid)s, %(aid)s, %(email)s, %(firstName)s, %(lastName)s, %(fullName)s)''',
                {
                    'oid': identifier,
                    'aid': accountId,
                    'email': email,
                    'firstName': firstName,
                    'lastName': lastName,
                    'fullName': fullName
                })
            
        with_cursor(_create)
        
    @classmethod
    def update(cls, identifier, email, firstName, lastName, fullName):
        
        def _update(cursor):
            cursor.execute(
                '''update openid_accounts set email = %(email)s, \
first_name = %(firstName)s, last_name = %(lastName)s, full_name = %(fullName)s \
where openid_identifier like %(oid)s''',
                {
                    'oid': identifier,
                    'email': email,
                    'firstName': firstName,
                    'lastName': lastName,
                    'fullName': fullName
                })
            
            
        with_cursor(_update)
        
        
        
        
        
        