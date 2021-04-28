from shellfm import WindowController


def main():
    window_controller = WindowController()

    # Create "File Window" 1
    window          = window_controller.create_window()
    window.nickname = "Win1"
    window_controller.add_view_for_window_by_nickname(window.nickname)

    # Create "File Window" 2
    window2          = window_controller.create_window()
    window2.nickname = "Win2"
    window_controller.add_view_for_window_by_nickname(window2.nickname)

    window_controller.list_windows()


if __name__ == '__main__':
    main()
