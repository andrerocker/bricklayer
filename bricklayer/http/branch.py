from cyclone.web import RequestHandler

class BranchController(cyclone.web.RequestHandler):
    def get(self, project_name):
        project = Projects(project_name)
        git = Git(project)
        branches = git.branches(remote=True)
        self.write(cyclone.escape.json_encode({'branches': branches}))

    def post(self, project_name):
        branch = self.get_argument('branch')
        project = Projects(project_name)
        if branch in project.branches():
            self.write(cyclone.escape.json_encode({'status': 'failed: branch already exist'}))
        else:
            project.add_branch(branch)
            project.version(branch, '0.1')
            reactor.callInThread(build_project, {'project': project.name, 'branch': self.get_argument('branch'), 'release': 'experimental'})
            self.write(cyclone.escape.json_encode({'status': 'ok'}))

    def delete(self, project_name):
        project = Projects(project_name)
        branch = self.get_argument('branch')
        project.remove_branch(branch)
        self.write(cyclone.escape.json_encode({'status': 'ok'}))


