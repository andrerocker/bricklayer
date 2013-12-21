from twisted.python import log

from cyclone import escape
from cyclone.web import RequestHandler

from model.project import Project

def _project_json(project, branch):
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

class ProjectIndexController(RequestHandler):

    def get(self, branch="master"):
        projects = Project.get_all()
        response = map(lambda current: _project_json(current, branch), projects)
        self.write(escape.json_encode(response))

class ProjectController(RequestHandler):

    def get(self, name, branch="master"):
        project = Project(name)
        json = _project_json(project, branch)
        self.write(escape.json_encode(json))

    def post(self, name):
        if Project(name).exists():
            self.write(escape.json_encode({"status":  "Project already exists"}))
            return

        try:
            project = Project()
            project.name = name
            project.git_url = self.get_argument('git_url')[0]
            project.group_name = self.get_argument('group_name')
            project.save()
            self.write(escape.json_encode({"status": "ok"}))
            log.msg('Project created:', project.name)
        except Exception, e:
            log.err()
            self.write(escape.json_encode({"status": "fail"}))

    # def put(self, name):
    #     project = Projects(name)
    #     try:
    #         for aname, arg in self.request.arguments.iteritems():
    #             if aname in ('branch'):
    #                 branch = arg
    #             else:
    #                 setattr(project, aname, arg[0])

    #         json_data = json.loads(self.request.body)
    #         if len(json_data.keys()) > 0:
    #             for k, v in json_data.iteritems():
    #                 setattr(project, k, v)

    #         project.save()
    #     except Exception, e:
    #         log.err(e)
    #         self.finish(escape.json_encode({'status': 'fail'}))
    #     self.finish(escape.json_encode({'status': 'modified %s' % name}))


    # def delete(self, name):
    #     log.msg("deleting project %s" % name)
    #     try:
    #         project = Projects(name)
    #         git = Git(project)
    #         git.clear_repo()
    #         project.clear_branches()
    #         project.delete()
    #         self.write(escape.json_encode({'status': 'project deleted'}))
    #     except Exception, e:
    #         log.err(e)
    #         self.write(escape.json_encode({'status': 'failed to delete %s' % str(e)}))
