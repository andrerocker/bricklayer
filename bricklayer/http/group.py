
from cyclone import escape
from cyclone.web import RequestHandler

from model.group import Group

class GroupController(RequestHandler):
    def get(self, *args):
        groups_json = []
        groups = []

        if len(args) > 1:
            name = args[0]
            groups = [Group(name)]
        else:
            groups = Group.get_all()

        for group in groups:
            group_json = {}
            for attr in ('name', 'repo_addr', 'repo_user', 'repo_passwd'):
                group_json.update({attr: getattr(group, attr)})
            groups_json.append(group_json)
        self.write(escape.json_encode(groups_json))

    def post(self, *args):
        try:
            if len(args) > 0:
                name = args[0]
                group = Group(name)
                for key, value in self.request.arguments.iteritems():
                    if key in ("repo_addr", "repo_user", "repo_passwd"):
                        setattr(group, key, value[0])
                group.save()
            else:
                group = Group(self.get_argument('name'))
                group.repo_addr = self.get_argument('repo_addr')
                group.repo_user = self.get_argument('repo_user')
                group.repo_passwd = self.get_argument('repo_passwd')
                group.save()
            self.write(escape.json_encode({'status': 'ok'}))
        except Exception, e:
            self.write(escape.json_encode({'status': 'fail', 'error': str(e)}))