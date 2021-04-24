from .view import View


class Window:
    def __init__(self):
        self.name     = ""
        self.nickname = ""
        self.id       = 0
        self.views    = []

    def create_view(self):
        view = View()
        self.views.append(view)
        return view

    def pop_view(self):
        self.views.pop()

    def delete_view(self, vid):
        i = -1
        for view in self.views:
            i += 1
            if view.id == vid:
                del self.views[i]
                break


    def get_view_by_id(self, vid):
        for view in self.views:
            if view.id == vid:
                return view

    def get_view_by_index(self, index):
        return self.views[index]
