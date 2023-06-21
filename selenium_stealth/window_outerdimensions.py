
from work_fs import path_in_exefile
from .wrapper import evaluateOnNewDocument
from selenium.webdriver import Chrome as Driver


def window_outerdimensions(driver: Driver, **kwargs) -> None:
    js_path = path_in_exefile()
    file_js_path = js_path / "js" / "window.outerdimensions.js"

    evaluateOnNewDocument(
        driver, file_js_path.read_text()
    )
