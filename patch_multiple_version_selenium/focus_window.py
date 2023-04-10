import time

from pywinauto import Application


def auto_focus_every_30(path_to_chrome):
    app = Application().connect(path=path_to_chrome)

    while True:
        time.sleep(30)
        main_window = app.top_window()
        main_window.set_focus()
