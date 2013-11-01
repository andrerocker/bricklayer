from zope.interface import implements

from twisted.python import usage
from twisted.plugin import IPlugin
from twisted.application.service import IServiceMaker

import bricklayer.rest

class MyServiceMaker(object):
    implements(IServiceMaker, IPlugin)
    options = usage.Options
    tapname = "bricklayer_web"
    description = "Bricklayer WebService."

    def makeService(self, config):
        print bricklayer.__file__
        return bricklayer.rest.server

serviceMaker = MyServiceMaker()
