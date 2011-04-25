import logging
from pprint import pprint, pformat

import cherrypy
import psycopg2.pool

class SetupPgConnectionPool(cherrypy.process.plugins.SimplePlugin):
    
    def __init__(self, pool_name, db_name, db_user):
        super(SetupPgConnectionPool, self).__init__(bus=cherrypy.engine)
        self.__pool_name = self.get_full_pool_name(pool_name)
        self.__db_name = db_name
        self.__db_user = db_user
        
    def start(self):
        cherrypy.log.error('Inside start', 'SetupPgConnectionPool', logging.DEBUG)
        self.__setup_connection_pool()
        
    def stop(self):
        cherrypy.log.error('Inside stop', 'SetupPgConnectionPool', logging.DEBUG)
        self.__cleanup_connection_pool()
        
    def graceful(self):
        cherrypy.log.error('Inside graceful', 'SetupPgConnectionPool', logging.DEBUG)
        self.__cleanup_connection_pool()
        self.__setup_connection_pool()
        
    def __setup_connection_pool(self):
        cherrypy.log.error('Inside __setup_connection_pool', 'SetupPgConnectionPool', logging.DEBUG)
        app = cherrypy.tree.apps['']
        pool = psycopg2.pool.ThreadedConnectionPool(
            minconn=3,
            maxconn=10,
            database=self.__db_name,
            user=self.__db_user)
        setattr(app, self.__pool_name, pool)
        
    def __cleanup_connection_pool(self):
        cherrypy.log.error('Inside __cleanup_connection_pool', 'SetupPgConnectionPool', logging.DEBUG)
        app = cherrypy.tree.apps['']
        if hasattr(app, self.__pool_name):
            cherrypy.log.error('Closing db connections')
            pool = getattr(app, self.__pool_name)
            pool.closeall()
        else:
            cherrypy.log.error('No db connection pool')
            
    @classmethod
    def get_full_pool_name(cls, pool_name):
        return '{0}_pg_connection_pool'.format(pool_name)
            