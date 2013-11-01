class Build(cyclone.web.RequestHandler):
    def post(self, project_name):
        project = Projects(project_name)
        release = self.get_argument('tag')
        version = self.get_argument('version')
        commit = self.get_argument('commit', default='HEAD')

        reactor.callInThread(build_project, {
                    'project': project.name,
                    'branch' : 'master',
                    'release': release,
                    'version': version,
                    'commit' : commit,
        })

        self.write(cyclone.escape.json_encode({'status': 'build of branch %s scheduled' % release}))

    def get(self, project_name):
        project = project_name
        build_ids = BuildInfo(project, -1).builds()
        builds = []
        for bid in build_ids[-10:]:
            build = BuildInfo(project, bid)
            builds.append({'build': int(bid), 'log': os.path.basename(build.log()), 'version': build.version(), 'release': build.release(), 'date': build.time()})
        self.write(cyclone.escape.json_encode(builds))


