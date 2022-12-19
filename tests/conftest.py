import pytest
import uuid
from selenium.webdriver import Chrome

@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    # This function helps to detect that some test failed
    # and pass this information to teardown:

    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep

@pytest.fixture
def web_browser():

    browser = Chrome(executable_path=r'D:\skillfactory\lesson_19.7.2\tests\chromedriver.exe')

    browser.implicitly_wait(5)

    # Return browser instance to test case:
    yield browser

    browser.quit()

