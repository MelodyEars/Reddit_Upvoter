
from work_fs import path_in_exefile
from .wrapper import evaluateOnNewDocument
from selenium.webdriver import Chrome as Driver


def webgl_vendor_override(
    driver: Driver,
    webgl_vendor: str,
    renderer: str,
    **kwargs
) -> None:

    js_path = path_in_exefile()
    file_js_path = js_path / "js" / 'webgl.vendor.js'

    evaluateOnNewDocument(
        driver, file_js_path.read_text(),
        webgl_vendor,
        renderer,
    )
