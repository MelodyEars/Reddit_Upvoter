import time

from pywinauto import Application


# Process 1(tgBOT and browsers)
def add_process(browser_pid, LIST_PID_BROWSERS):
    app = Application().connect(process=browser_pid)
    main_window = app.top_window()
    # main_window.set_focus()
    if main_window not in LIST_PID_BROWSERS:
        LIST_PID_BROWSERS.append(main_window)


# Process 2
def call_auto_focus(LIST_PID_BROWSERS):
    while len(LIST_PID_BROWSERS) <= 1:  # wait start process
        print("wait more window")
        time.sleep(5)

    while LIST_PID_BROWSERS:
        for main_window in LIST_PID_BROWSERS:
            print(f"Select: {main_window}")
            try:
                main_window.set_focus()
                time.sleep(5)
            except RuntimeError:
                LIST_PID_BROWSERS.remove(main_window)
