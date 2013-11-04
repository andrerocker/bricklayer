import os
import sys
import logging

from twisted.python import log
from twisted.protocols import basic
from twisted.application import internet, service
from twisted.internet import protocol, task, threads, reactor, defer

import builder
from builder import Builder
from builder import build_project

from model.project import Project

from git import Git
from config import BrickConfig

class BricklayerService(service.Service):

    def __init__(self):
        log.msg("scheduler: init")
        self.sched_task = task.LoopingCall(self.sched_builder)
    
    def send_job(self, project_name, branch, release, version):
        log.msg('sched build: %s [%s:%s]' % (project_name, release, version))
        brickconfig = BrickConfig()
        builder.build_project({
            'project': project_name, 
            'branch': branch, 
            'release': release, 
            'version': version,
        })

    def sched_builder(self):
        for project in sorted(Project.get_all(), key=lambda p: p.name):
            if (project.name == ""):
                continue
            try:
                log.msg("checking project: %s" % project.name)
                if project.is_building():
                    log.msg("project %s still building, skip" % project.name)
                    continue

                branch = "master"
                git = Git(project)
                if os.path.isdir(git.workdir):
                    git.checkout_branch(branch)
                    git.pull()
                else:
                    git.clone(branch)

                if not os.path.isdir(git.workdir):
                    continue

                for remote_branch in git.branches(remote=True):
                    git.checkout_remote_branch(remote_branch.replace('origin/', ''))

                for release in ('stable', 'testing', 'unstable'):
                    if project.last_tag(release) != git.last_tag(release):
                        try:
                            _, version = git.last_tag(release).split('_')
                            log.msg("new %s tag, building version: %s" % (release, version))
                            d = threads.deferToThread(self.send_job, project.name, branch, release, version)
                        except Exception, e:
                            log.msg("tag not parsed: %s:%s" % (project.name, git.last_tag(release)))

            except Exception, e:
                log.err(e)
                

    def startService(self):
        service.Service.startService(self)
        log.msg("scheduler: start %s" % self.sched_task)
        self.sched_task.start(10.0)

    @defer.inlineCallbacks
    def stopService(self):
        service.Service.stopService(self)
        yield self.sched_task.stop()

application  = service.Application("Bricklayer")
brickService = BricklayerService()
brickService.setServiceParent(application)