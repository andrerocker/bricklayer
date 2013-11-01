class Current(cyclone.web.RequestHandler):
    def get(self):
        response = []
        currents = CurrentBuild.get_all()
        for current in currents:
            response.append({"name":current.name})
        self.set_header("Content-Type", "application/json")
        self.write(cyclone.escape.json_encode(response))

    def delete(self):
        CurrentBuild.delete_all()
        self.write(cyclone.escape.json_encode("ok"))
