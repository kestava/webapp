from lib.errors import NotImplementedError, ApplicationError
from database import with_cursor

class Account(object):

    @classmethod
    def get_account_id_by_email(cls, email, cursor=None):

        def _get(cursor):
            _get.result = None
            cursor.execute(
                'select account_id from accounts where email like %(email)s',
                {'email': email})
            
            row = cursor.fetchone()
            if row:
                _get.result = row['account_id']
        
        if cursor is None:
            with_cursor(_get)
        else:
            _get(cursor)
            
        return _get.result
            
    @classmethod
    def create(cls, email, cursor=None):
        id = None
        
        if cursor is None:
            raise NotImplementedError('Account.create without cursor')
        
        else:
            cursor.execute(
                'insert into accounts (email) values (%(email)s) returning account_id',
                {'email': email})
            
            row = cursor.fetchone()
            
            if row is None:
                raise ApplicationError('account row not inserted')
                
            id = row['account_id']
            
        print('accounts record with account_id={0} created'.format(id))    
        return id
                
                