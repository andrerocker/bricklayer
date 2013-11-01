import os
import sys
import json
import signal

from git import Git
from groups import Groups
from config import BrickConfig
from projects import Projects

from builder import Builder, build_project
from build_info import BuildInfo
from current_build import CurrentBuild

import cyclone.web
import cyclone.escape

from twisted.python import log
from twisted.internet import reactor
from twisted.application import service, internet

from http.main import Main
from http.project import Project

brickconfig = BrickConfig()

restApp = cyclone.web.Application([
    (r'/static/(.*)', cyclone.web.StaticFileHandler, {'path': brickconfig.get('static', 'dir')}),
    (r'/project', Project),
    # (r'/project/?(.*)', Project),
    # (r'/branch/(.*)', Branch),
    # (r'/clear/(.*)', Clear),
    # (r'/build/current', Current),
    # (r'/build/(.*)', Build),
    # (r'/group', Group),
    # (r'/group/?(.*)', Group),
    # (r'/log/(.*)/+(.*)', Log),
    # (r'/repo/(.*)', cyclone.web.StaticFileHandler, {'path': brickconfig.get('local_repo', 'dir')}),
    (r'/', Main)
])

application = service.Application("bricklayer_rest")
server = internet.TCPServer(int(brickconfig.get('server', 'port')), restApp, interface="0.0.0.0")
server.setServiceParent(application)
