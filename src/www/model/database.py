import cherrypy

from psycopg2 import connect
from psycopg2.extras import DictCursor

# It's best practice to create a single connection and use it throughout the
# life of the request. It's also okay to create multiple cursors, as opposed
# to creating a single cursor reusing it.
#
# Reference: http://initd.org/psycopg/docs/faq.html#best-practices

def make_connection():
    settings = cherrypy.request.app.config['appSettings']
    cherrypy.request.db = connect(
        database=settings['mainDatabaseName'],
        user=settings['mainDatabaseUser'],
        password=settings['mainDatabasePassword'])
    
def close_connection():
    cherrypy.request.db.commit()
    cherrypy.request.db.close()
            
def with_cursor(func, *args, **kwargs):
    cursor = cherrypy.request.db.cursor(cursor_factory=DictCursor)
    try:
        return func(cursor, *args, **kwargs)
    finally:
        cursor.close()
        cherrypy.request.db.commit()