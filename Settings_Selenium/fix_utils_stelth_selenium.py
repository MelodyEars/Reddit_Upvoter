import pkg_resources

from .wrapper import evaluateOnNewDocument
from selenium.webdriver import Chrome as Driver

def with_utils(driver: Driver, **kwargs) -> None:
    utils_js = pkg_resources.resource_string(__name__, "js/utils.js").decode("utf-8")
    evaluateOnNewDocument(driver, utils_js)
