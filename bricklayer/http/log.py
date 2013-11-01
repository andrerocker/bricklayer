class Log(cyclone.web.RequestHandler):
    def get(self, project, bid):
        build_info = BuildInfo(project, bid)
        if os.path.isfile(build_info.log()):
            self.write(open(build_info.log()).read())
