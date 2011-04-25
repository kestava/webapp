"""
.. automodule:: model.modelobjectbase
.. automodule:: model.openidaccount
.. automodule:: model.modelobjectbase
.. automodule:: model.sitedata
.. automodule:: model.testing
.. automodule:: model.userdata
.. automodule:: model.userdatatheme
"""

from pprint import pprint, pformat
import logging

import cherrypy
from psycopg2.extras import DictCursor

from plugins.setuppgconnectionpool import SetupPgConnectionPool

def load_model(classes):
    o = {}
        
    for i in classes:
        a = i()
        if a.key in o:
            o[a.key].update(a.read())
        else:
            o[a.key] = a.read()
            
    return o
    
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
    cur.execute(trim_statement(statement), variables)
    return cur.fetchone()
    
def get_row_nc(pool_name, statement, variables):
    """
    Like get_row, but doesn't require a connection to be passed in as an
    argument.
    
    Useful when not wrapping multiple statements in a transaction.
    """
    with grab_connection(pool_name) as conn:
        return get_row(conn, statement, variables)
    
def trim_statement(input):
    """
    Produces a neatened SQL statement
    """
    cherrypy.log.error(
        'Transforming: {0}'.format(input),
        'trim_statement',
        logging.DEBUG)
    
    o = []
    for i in input.splitlines()[:]:
        a = i.strip()
        if '' != a:
            o.append(a)
    
    p = ' '.join(o)
    
    cherrypy.log.error(
        'Returning: {0}'.format(p),
        'trim_statement',
        logging.DEBUG)
            
    return p
    