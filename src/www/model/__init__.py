"""
.. automodule:: model.credits
.. automodule:: model.itemdata
.. automodule:: model.modelobjectbase
.. automodule:: model.openidaccount
.. automodule:: model.sitedata
.. automodule:: model.testing
.. automodule:: model.userdata
.. automodule:: model.usersettings
"""

from pprint import pprint, pformat
import logging

import cherrypy
from psycopg2.extras import DictCursor

from plugins.setuppgconnectionpool import SetupPgConnectionPool

def load_model(includes):
    o = {}
        
    for i in includes:
        if i.key in o:
            o[i.key].update(i.read())
        else:
            o[i.key] = i.read()
            
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
        
def get_scalar_nc(pool_name, statement, variables, column):
    with grab_connection(pool_name) as conn:
        return get_scalar(conn, statement, variables, column)
        
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

def get_all_rows_nc(pool_name, statement, variables):
    with grab_connection(pool_name) as conn:
        return get_all_rows(conn, statement, variables)
        
def get_all_rows(connection, statement, variables):
    cur = connection.cursor(cursor_factory=DictCursor)
    cur.execute(trim_statement(statement), variables)
    return cur.fetchall()
    
def execute_action_nc(pool_name, statement, variables, return_row=False):
    with grab_connection(pool_name) as conn:
        return execute_action(conn, statement, variables, return_row)
        
def execute_action(connection, statement, variables, return_row=False):
    cur = connection.cursor(cursor_factory=DictCursor)
    cur.execute(trim_statement(statement), variables)
    if return_row:
        return cur.fetchone()
    
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
    