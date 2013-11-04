from cyclone import escape
from cyclone.web import RequestHandler

class ClearController(RequestHandler):
    def post(self, project):
        try:
            self._clear_repo(Project(project))
            self.write(escape.json_encode({'status': 'ok'}))
        except Exception, e:
            self.write(escape.json_encode({'status': 'fail', 'error': str(e)}))

	def _clear_repo(self, project):
		Git(project).clear_repo()