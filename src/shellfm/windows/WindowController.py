# Python imports
import json
from os import path

# Lib imports


# Application imports
from . import Window


class WindowController:
    def __init__(self):
        self.windows     = []

        USER_HOME        = path.expanduser('~')
        CONFIG_PATH      = USER_HOME + "/.config/pyfm"
        self.config_file = CONFIG_PATH + "/session.json"


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
        self.windows.append(window)

    def add_view_for_window(self, win_id):
        for window in self.windows:
            if window.id == win_id:
                return window.create_view()

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


    def list_files_from_views_of_window(self, win_id):
        for window in self.windows:
            if window.id == win_id:
                for view in window.views:
                    print(view.files)
                break

    def get_views_count(self, win_id):
        for window in self.windows:
            if window.id == win_id:
                return len(window.views)

    def return_views_from_window(self, win_id):
        for window in self.windows:
            if window.id == win_id:
                return window.views

    def save_state(self):
        windows = []
        for window in self.windows:
            views = []
            for view in window.views:
                views.append(view.get_current_directory())

            windows.append(
                [
                    {
                        'window':{
                            "ID": str(window.id),
                            "Name": window.name,
                            "Nickname": window.nickname,
                            'views': views
                        }
                    }
                ]
            )

        with open(self.config_file, 'w') as outfile:
            json.dump(windows, outfile, separators=(',', ':'), indent=4)

    def load_state(self):
        if path.isfile(self.config_file):
            with open(self.config_file) as infile:
                return json.load(infile)
