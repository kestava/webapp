
import cherrypy

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