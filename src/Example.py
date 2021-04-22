from shellfm import WindowController


def main():
    window_controller = WindowController()

    # Create "File Window" 1
    window_controller.add_window()
    window_controller.add_view_for_window(1)

    # Create "File Window" 2
    window_controller.add_window()
    window_controller.add_view_for_window(2)

    window_controller.list_windows()


if __name__ == '__main__':
    main()
