class Clear(cyclone.web.RequestHandler):
    def post(self, project_name):
        try:
            project = Projects(project_name)
            git = Git(project)
            git.clear_repo()
            self.write(cyclone.escape.json_encode({'status': 'ok'}))
        except Exception, e:
            self.write(cyclone.escape.json_encode({'status': 'fail', 'error': str(e)}))
