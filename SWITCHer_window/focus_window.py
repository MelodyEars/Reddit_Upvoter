import time
from loguru import logger
from pywinauto import Application


def auto_focus_every_30(pid):
    app = Application().connect(process=pid)
    main_window = app.top_window()
    # main_window.set_focus()

    while True:
        try:
            main_window.set_focus()
        except RuntimeError:
            logger.info(f"Автофокус вимкнут для {pid}")
            break

        time.sleep(5)
