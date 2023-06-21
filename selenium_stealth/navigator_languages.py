
from work_fs import path_in_exefile
from .wrapper import evaluateOnNewDocument
from selenium.webdriver import Chrome as Driver


def navigator_languages(driver: Driver, languages: [str], **kwargs) -> None:
    js_path = path_in_exefile()
    file_js_path = js_path / "js" / "navigator.languages.js"

    evaluateOnNewDocument(driver, file_js_path.read_text(), languages,)