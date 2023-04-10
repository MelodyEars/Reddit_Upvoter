import time

from pywinauto import Application

# PID_ALL_BROWSER = []


def auto_focus_every_30(pid):
    app = Application().connect(process=pid)
    while True:
        time.sleep(30)

        try:
            main_window = app.top_window()
            main_window.set_focus()
        except Exception:
            return
