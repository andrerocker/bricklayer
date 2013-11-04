from git import Git
from config import BrickConfig

# from builder import Builder, build_project
# from build_info import BuildInfo
# from current_build import CurrentBuild

import cyclone.escape
from cyclone.web import Application

from twisted.python import log
from twisted.internet import reactor
from twisted.application import service, internet

from http.main import MainController
from http.build import BuildController
from http.group import GroupController
from http.project import ProjectController

def draw_routes():
    return Application([
        (r'/static/(.*)', cyclone.web.StaticFileHandler, {'path': brickconfig.get('static', 'dir')}),
        (r'/project', ProjectController),
        (r'/project/?(.*)', ProjectController),
        (r'/group', GroupController),
        (r'/build/(.*)', BuildController),        
        # (r'/build/current', Current),
        # (r'/group/?(.*)', Group),
        # (r'/branch/(.*)', Branch),
        # (r'/clear/(.*)', Clear),
        # (r'/log/(.*)/+(.*)', Log),
        # (r'/repo/(.*)', cyclone.web.StaticFileHandler, {'path': brickconfig.get('local_repo', 'dir')}),
        (r'/', MainController)
    ])

def start(application):
    server = internet.TCPServer(int(brickconfig.get('server', 'port')), draw_routes(), interface="0.0.0.0")
    server.setServiceParent(application)

brickconfig = BrickConfig()
application = service.Application("bricklayer_rest")

start(application)