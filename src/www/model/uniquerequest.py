
import os
import binascii

from model import grab_connection, execute_action, execute_action_nc
from model import get_scalar_nc

class UniqueRequest(object):
    
    def create(self, sessionKey, requestKey, data=None):
        """
        Creates a database record in the unique_requests table foor the
        requestKey/sessionKey combination and returns the unique value
        generated.
        """        
        value = binascii.hexlify(os.urandom(20)).decode('ascii')
        print('Random value: {0}'.format(value))
        
        with grab_connection('main') as connection:
            execute_action(connection,
                """
                delete from unique_requests
                where session_key = %(s)s and request_key = %(r)s
                """,
                { 's': sessionKey, 'r': requestKey })
            
            execute_action(connection,
                """
                insert into unique_requests
                (session_key, request_key, request_value)
                values (%(s)s, %(r)s, %(v)s)
                """,
                { 's': sessionKey, 'r': requestKey, 'v': value })
            
            if data:
                execute_action(connection,
                    """
                    update unique_requests
                    set request_data = %(d)s
                    where session_key = %(s)s and request_key = %(r)s
                    """,
                    { 'd': data, 's': sessionKey, 'r': requestKey })
            
        return value
    
    def exists(self, sessionKey, requestKey, value):
        return get_scalar_nc(
            'main',
            """
            select exists (select 0 from unique_requests
            where
            session_key = %(s)s
            and request_key = %(r)s
            and request_value = %(v)s) as a
            """,
            { 's': sessionKey, 'r': requestKey, 'v': value },
            'a')
        
    def delete(self, connection, sessionKey, requestKey):
        execute_action(
            connection,
            """
            delete from unique_requests
            where session_key = %(s)s and request_key = %(r)s
            """,
            { 's': sessionKey, 'r': requestKey })
        
    def get_data(self, sessionKey, requestKey):
        return get_scalar_nc(
            'main',
            """
            select a.request_data
            from unique_requests as a
            where a.session_key = %(s)s and a.request_key = %(r)s
            """,
            { 's': sessionKey, 'r': requestKey },
            'request_data')
    