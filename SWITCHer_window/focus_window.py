import time

from pywinauto import Application


# Process 2
def call_auto_focus(LIST_PID_BROWSERS):
    while len(LIST_PID_BROWSERS) != 0:  # wait start process
        print("wait more window")
        time.sleep(5)

    while LIST_PID_BROWSERS:
        # if len(LIST_PID_BROWSERS) != 1:
        for browser_pid in LIST_PID_BROWSERS:
            try:
                print(f"Select: {browser_pid}")
                app = Application().connect(process=browser_pid)
                main_window = app.top_window()

                main_window.set_focus()
                time.sleep(5)
            except RuntimeError:
                print(f"Delete: {browser_pid}")
                LIST_PID_BROWSERS.remove(browser_pid)
        # else:
        #     time.sleep(5)
