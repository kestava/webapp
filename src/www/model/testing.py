
from pprint import pprint, pformat

import psycopg2.extras
import cherrypy

from model import grab_connection

def quick_test():
    Animal.delete_all()
    Animal.insert_several()
    cherrypy.log.error('Animals:\n{0}'.format(pformat(Animal.get_all())))
    
class Animal(object):
    
    @classmethod
    def get_all(cls):
        with grab_connection('main') as conn:
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cursor.execute('select * from testing.animals')
            return cursor.fetchall()
    
    @classmethod
    def insert_several(cls):
        with grab_connection('main') as conn:
            data = [{'n': 'zebra'}, {'n': 'gorilla'}, {'n': 'honey bee'}]
            cursor = conn.cursor()
            cursor.executemany('insert into testing.animals (animal_name) values (%(n)s)', data)
    
    @classmethod
    def delete_all(cls):
        with grab_connection('main') as conn:
            cursor = conn.cursor()
            cursor.execute('delete from testing.animals')
            