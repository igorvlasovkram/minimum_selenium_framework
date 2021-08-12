from __future__ import annotations
from typing import Callable, Any

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.android.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ChromeOptions

options = ChromeOptions()
options.headless = True
driver = webdriver.Chrome(
    executable_path=ChromeDriverManager().install(),
    options=options
)


def wait():
    return WebDriverWait(
        driver,
        4,
        poll_frequency=0.1,
        ignored_exceptions=WebDriverException
    )


class empty_value_in_element:
    def __init__(self, selector: str):
        self.selector = selector

    def __call__(self, driver: WebDriver):
        return driver.find_element_by_css_selector(self.selector)\
                   .get_attribute('value') == ''


class element_exact_text:
    def __init__(self, selector: str, text):
        self.selector = selector
        self.text = text

    def __call__(self, driver: WebDriver):
        return driver.find_element_by_css_selector(self.selector)\
                   .text == self.text


class element_exact_attribute_value:
    def __init__(self, selector: str, name: str, text):
        self.selector = selector
        self.name = name
        self.text = text

    def __call__(self, driver: WebDriver):
        return driver.find_element_by_css_selector(self.selector) \
                   .get_attribute(self.name) == self.text


class element_command_passed:
    def __init__(self, selector: str, command: Callable[[WebElement], Any]):
        self.selector = selector
        self.command = command

    def __call__(self, driver: WebDriver):
        self.command(driver.find_element_by_css_selector(self.selector))
        return True


def visit(url: str):
    driver.get(url)


def close():
    driver.quit()


def should_have_title_containing(value: str):
    wait().until(expected_conditions.title_contains(value))


class Element:
    def __init__(self, selector: str):
        self.selector = selector

    def should_have_exact_text(self, text):
        wait().until(element_exact_text(self.selector, text))
        return self

    def should_have_attribute(self, name: str, text):
        wait().until(element_exact_attribute_value(self.selector, name, text))
        return self

    def should_be_blank(self):
        return self.should_have_exact_text('')\
            .should_have_attribute('value', '')

    def clear(self):
        wait().until(element_command_passed(
            self.selector,
            lambda it: it.clear()
        ))
        return self

    def type(self, text):
        wait().until(element_command_passed(
            self.selector,
            lambda it: it.send_keys(text)
        ))
        return self

    def set_value(self, text):
        self.clear()
        return self.type(text)

    def press_enter(self):
        wait().until(element_command_passed(
            self.selector,
            lambda it: it.send_keys(Keys.ENTER)
        ))

def element(selector: str) -> Element:
    return Element(selector)
