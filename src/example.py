# Python imports
import builtins
import threading


# NOTE: Threads WILL NOT die with parent's destruction.
def threaded_wrapper(fn):
    def wrapper(*args, **kwargs):
        threading.Thread(target=fn, args=args, kwargs=kwargs, daemon=False).start()
    return wrapper

# NOTE: Threads WILL die with parent's destruction.
def daemon_threaded_wrapper(fn):
    def wrapper(*args, **kwargs):
        threading.Thread(target=fn, args=args, kwargs=kwargs, daemon=True).start()
    return wrapper

# NOTE: Defined for ShellFM
builtins.threaded        = threaded_wrapper
builtins.daemon_threaded = daemon_threaded_wrapper


# Lib imports

# Apoplication imports
from shellfm.windows.controller import WindowController
from libs.logger import Logger



builtins.logger          = Logger("./", _ch_log_lvl = 10, _fh_log_lvl = 10).get_logger()



def main():
    window_controller = WindowController()

    # Create "File Window" 1
    window          = window_controller.create_window()
    window.set_nickname("Win1")
    window_controller.add_tab_for_window_by_nickname(window.get_nickname())

    # Create "File Window" 2
    window2          = window_controller.create_window()
    window2.set_nickname("Win2")
    window_controller.add_tab_for_window_by_nickname(window2.get_nickname())

    window_controller.list_windows()


    window2.set_is_hidden(True)
    window_controller.list_windows()
    logger.info("-- Finished Example Run --")


if __name__ == '__main__':
    main()
