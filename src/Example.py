from shellfm.windows.controller import WindowController


def main():
    print("\n\n-------------------------------------------\n\n")
    window_controller = WindowController()

    # Create "File Window" 1
    window          = window_controller.create_window()
    window.set_nickname("Win1")
    window_controller.add_view_for_window_by_nickname(window.get_nickname())

    # Create "File Window" 2
    window2          = window_controller.create_window()
    window2.set_nickname("Win2")
    window_controller.add_view_for_window_by_nickname(window2.get_nickname())

    window_controller.list_windows()


    print("\n\n-------------------------------------------\n\n")
    window2.set_is_hidden(True)
    window_controller.list_windows()


if __name__ == '__main__':
    main()
