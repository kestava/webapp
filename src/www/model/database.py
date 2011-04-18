
import cherrypy
from psycopg2.extras import DictCursor

from plugins.setuppgconnectionpool import SetupPgConnectionPool

class ConnectionManager(object):

    def __init__(self, pool_name, auto_commit=True):
        pool_name = SetupPgConnectionPool.get_full_pool_name(pool_name)
        self.__pool = getattr(cherrypy.request.app, pool_name)
        self.__auto_commit = auto_commit

    def __enter__(self):
        self.__conn = self.__pool.getconn()
        return self.__conn
            
    def __exit__(self, exc_type, exc_value, traceback):
        if self.__auto_commit:
            self.__conn.commit()
        self.__pool.putconn(self.__conn)
    
def grab_connection(pool_name, auto_commit=True):
    return ConnectionManager(pool_name, auto_commit)
    
def get_scalar(connection, statement, variables, column):
    data = get_row(connection, statement, variables)
    if not data is None:
        return data[column]
        
def get_row(connection, statement, variables):
    cur = connection.cursor(cursor_factory=DictCursor)
    cur.execute(statement, variables)
    return cur.fetchone()