from .import View


class Window:
    def __init__(self):
        self.name     = ""
        self.nickname = ""
        self.id       = 0
        self.views    = []

    def create_view(self):
        view = View()
        self.views.append(view)

    def pop_view(self):
        self.views.pop()

    def delete_view(self, index):
        del self.views[index]

    def get_view(self, index):
        return self.views[index]
