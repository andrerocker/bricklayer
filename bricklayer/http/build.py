from cyclone import escape
from cyclone.web import RequestHandler

from model.project import Project
from model.build_info import BuildInfo

class BuildController(RequestHandler):
    def get(self, name):
        project = name
        build_ids = BuildInfo(project, -1).builds()
        builds = []
        for bid in build_ids[-10:]:
            build = BuildInfo(project, bid)
            builds.append({'build': int(bid), 'log': os.path.basename(build.log()), 'version': build.version(), 'release': build.release(), 'date': build.time()})
        self.write(escape.json_encode(builds))

    def post(self, name):
        project = Project(name)
        release = self.get_argument('tag')
        version = self.get_argument('version')
        commit  = self.get_argument('commit', default='HEAD')

        reactor.callInThread(build_project, {
            'project': project.name,
            'branch' : 'master',
            'release': release,
            'version': version,
            'commit' : commit,
        })

        self.write(escape.json_encode({'status': 'build of branch %s scheduled' % release}))