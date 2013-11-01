from cyclone import escape
from cyclone.web import RequestHandler

from projects import Projects

class Project(RequestHandler):

    def get(self, name=None, branch="master"):
        if name:
            response = _project_json(Projects(name))
        else:
            projects = Projects.get_all()
            response = []
            for project in projects:
                response.append(_project_json(project))
        if response:
            self.write(escape.json_encode(response))
        else:
            self.write(escape.json_encode("%s No project found"))

    def post(self, *args):
        if len(args) >= 1:
            name = args[0]
            project = Projects(name)
            for key, value in self.request.arguments.iteritems():
                if key in ("git_url", "version", "build_cmd", "install_cmd"):
                    setattr(project, key, value[0])
            project.save()

        try:
            if not Projects(self.get_argument('name')).exists():
                raise
        except Exception, e:
            project = Projects()
            project.name = self.get_argument('name')[0]
            project.git_url = self.get_argument('git_url')[0]
            for name, parm in self.request.arguments.iteritems():
                if name not in ('branch', 'version'):
                    setattr(project, str(name), parm[0])
            try:
                project.add_branch(self.get_argument('branch'))
                project.version(self.get_argument('branch'), self.get_argument('version'))
                project.group_name = self.get_argument('group_name')
                project.save()
                log.msg('Project created:', project.name)

                self.write(cyclone.escape.json_encode({'status': 'ok'}))
            except Exception, e:
                log.err()
                self.write(cyclone.escape.json_encode({'status': "fail"}))

        else:
            self.write(cyclone.escape.json_encode({'status':  "Project already exists"}))

    def put(self, name):
        project = Projects(name)
        try:
            for aname, arg in self.request.arguments.iteritems():
                if aname in ('branch'):
                    branch = arg
                else:
                    setattr(project, aname, arg[0])

            json_data = json.loads(self.request.body)
            if len(json_data.keys()) > 0:
                for k, v in json_data.iteritems():
                    setattr(project, k, v)

            project.save()
        except Exception, e:
            log.err(e)
            self.finish(cyclone.escape.json_encode({'status': 'fail'}))
        self.finish(cyclone.escape.json_encode({'status': 'modified %s' % name}))


    def delete(self, name):
        log.msg("deleting project %s" % name)
        try:
            project = Projects(name)
            git = Git(project)
            git.clear_repo()
            project.clear_branches()
            project.delete()
            self.write(cyclone.escape.json_encode({'status': 'project deleted'}))
        except Exception, e:
            log.err(e)
            self.write(cyclone.escape.json_encode({'status': 'failed to delete %s' % str(e)}))

    def _project_json(project):
        return({
            'name': project.name,
            'branch': project.branches(),
            'experimental': int(project.experimental),
            'group_name': project.group_name,
            'git_url': project.git_url,
            'version': project.version(),
            'last_tag_testing': project.last_tag(tag_type='testing'),
            'last_tag_stable': project.last_tag(tag_type='stable'),
            'last_tag_unstable': project.last_tag(tag_type='unstable'),
            'last_commit': project.last_commit(branch)
        })
