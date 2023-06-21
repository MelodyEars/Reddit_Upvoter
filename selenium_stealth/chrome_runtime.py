from work_fs import path_in_exefile
from .wrapper import evaluateOnNewDocument
from selenium.webdriver import Chrome as Driver


def chrome_runtime(driver: Driver, run_on_insecure_origins: bool = False, **kwargs) -> None:
    js_path = path_in_exefile()
    file_js_path = js_path / "js" / "chrome.runtime.js"

    evaluateOnNewDocument(
        driver, file_js_path.read_text(),
        run_on_insecure_origins,
    )
