from . import Window


class WindowController:
    def __init__(self):
        self.windows = []
        self.add_window()

    def get_window(self, win_id):
        for window in self.windows:
            if window.id == win_id:
                return window

        raise("No Window by ID {} found!".format(win_id))

    def get_windows(self):
        return self.windows

    def add_window(self):
        window      = Window()
        window.id   = len(self.windows) + 1
        window.name = "window_" + str(window.id)
        window.create_view()
        self.windows.append(window)

    def add_view_for_window(self, win_id):
        for window in self.windows:
            if window.id == win_id:
                window.create_view()
                break

    def pop_window(self):
        self.windows.pop()

    def delete_window_by_id(self, win_id):
        i = 0
        for window in self.windows:
            if window.id == win_id:
                self.window.remove(win_id)
                break
            i += 1

    def set_window_nickname(self, win_id = None, nickname = ""):
        for window in self.windows:
            if window.id == win_id:
                window.nickname = nickname

    def list_windows(self):
        for window in self.windows:
            print("\n[  Window  ]")
            print("ID: " + str(window.id))
            print("Name: " + window.name)
            print("Nickname: " + window.nickname)
            print("View Count: " + str( len(window.views) ))


    def list_views_from_window(self, win_id):
        for window in self.windows:
            if window.id == win_id:
                for view in window.views:
                    print(view.files)
                break

    def return_views_from_window(self, win_id):
        for window in self.windows:
            if window.id == win_id:
                return window.views
