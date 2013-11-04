from cyclone.web import RequestHandler

class MainController(RequestHandler):
    def get(self):
        self.redirect('/static/index.html')
