from pathlib import Path

from work_fs import path_in_exefile
from .wrapper import evaluateOnNewDocument
from selenium.webdriver import Chrome as Driver


# def with_utils(driver: Driver, **kwargs) -> None:
#     evaluateOnNewDocument(
#         driver, Path(__file__).parent.joinpath("js/utils.js").read_text()
#     )
#
def with_utils(driver: Driver, **kwargs) -> None:
    utils_path = path_in_exefile(Path(__file__).parent / "js/utils.js")
    evaluateOnNewDocument(driver, utils_path.read_text())

