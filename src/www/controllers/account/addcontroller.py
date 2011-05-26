
from pprint import pprint, pformat

import cherrypy

from new.newcontroller import NewController
from new.emailcontroller import EmailController

class AddController(object):

    new = NewController()
    email = EmailController()
