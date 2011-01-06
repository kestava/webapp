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
    
    # Using IDENT authentication.  Only the database name and database username
    # need to be specified, but the database engine must be configured such that
    # the current OS user can access the named database and is mapped properly
    # to the database user.
    cherrypy.request.db = connect(
        database=settings['mainDb'],
        user=settings['mainDbUser'])
    
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