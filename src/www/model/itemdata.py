
import cherrypy

from modelobjectbase import ModelObjectBase
from model import get_all_rows_nc
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
        