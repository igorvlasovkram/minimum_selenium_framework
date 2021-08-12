import pytest
from minimum_selenium_framework.helpers import own_selene as browser

@pytest.fixture(scope='function', autouse=True)
def browser_management():
    yield
    browser.close()
