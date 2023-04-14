import time
from multiprocessing import Manager

from pywinauto import Application

# PID_AUTOFOCUS = Manager().list()
PID_AUTOFOCUS = []

# Process 1(tgBOT and browsers)
def add_process(browser_pid):
    app = Application().connect(process=browser_pid)
    main_window = app.top_window()
    # main_window.set_focus()
    if main_window not in PID_AUTOFOCUS:
        PID_AUTOFOCUS.append(main_window)


# Process 2
def call_auto_focus():
    while not PID_AUTOFOCUS:  # wait start process
        time.sleep(5)

    while PID_AUTOFOCUS:
        for main_window in PID_AUTOFOCUS:
            try:
                main_window.set_focus()
                time.sleep(5)
            except RuntimeError:
                PID_AUTOFOCUS.remove(main_window)
