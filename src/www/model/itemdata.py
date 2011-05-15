
from pprint import pprint

import cherrypy

from modelobjectbase import ModelObjectBase
from model import get_all_rows_nc, get_scalar_nc, execute_action_nc
from lib.sessionhelper import SessionHelper

class ItemData(ModelObjectBase):
    
    key = 'itemData'
    
    def __init__(self, spec):
        specs = {
            'userItemsAll': self.__get_all_user_items
        }
        
        self.__func = specs[spec]
            
    def read(self):
        return self.__func()
        
    def __get_all_user_items(self):
        s = SessionHelper()
        return {
            'userItemsAll': get_all_rows_nc(
                'main',
                'select item_id, title from items where ref_user_account_id = %(i)s',
                { 'i': s.userAccountId })
        }
        
    @classmethod
    def user_has_draft_item(cls, id):
        s = SessionHelper()
        return get_scalar_nc(
            'main',
            """
            select exists (select 0 from unsilo.draft_items
            where ref_user_account_id = %(i)s) as a
            """,
            { 'i': s.userAccountId },
            'a')
        
    @classmethod
    def create_user_draft_item(cls, id):
        """
        Create a new item record and return its item id
        """
        s = SessionHelper()
        execute_action_nc(
            'main',
            """
            insert into unsilo.draft_items (ref_user_account_id) values (%(i)s)
            """,
            { 'i': s.userAccountId })
        