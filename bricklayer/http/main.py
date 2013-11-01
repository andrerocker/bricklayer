from cyclone.web import RequestHandler

class Main(RequestHandler):
    def get(self):
        self.redirect('/static/index.html')
