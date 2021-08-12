from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())

def empty_value_in_element(selector):
    def call(driver):
        return driver.find_element_by_css_selector(selector)\
               .get_attribute('value') == ''
    return call


def test_on_google():
    try:
        driver.get('https://google.com')

        WebDriverWait(driver, 4).until(empty_value_in_element('[name=q]'))

        driver.find_element_by_css_selector('[name=q]')\
            .clear()
        driver.find_element_by_css_selector('[name=q]')\
            .send_keys('yashaka python selene')
        driver.find_element_by_css_selector('[name=q]')\
            .send_keys(Keys.ENTER)
    finally:
        driver.quit()
