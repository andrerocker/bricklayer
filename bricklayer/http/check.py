class CheckController(cyclone.web.RequestHandler):
    def post(self, project_name):
        project = Projects(project_name)
        builder = Builder(project_name)
        builder.build_project()
