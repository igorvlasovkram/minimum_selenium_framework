from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())

def is_element_have_empty_value(driver) -> bool:
    return driver.find_element_by_css_selector('[name=q]')\
               .get_attribute('value') == ''


def test_on_google():
    try:
        driver.get('https://google.com')

        WebDriverWait(driver, 4).until(is_element_have_empty_value)

        driver.find_element_by_css_selector('[name=q]')\
            .clear()
        driver.find_element_by_css_selector('[name=q]')\
            .send_keys('yashaka python selene')
        driver.find_element_by_css_selector('[name=q]')\
            .send_keys(Keys.ENTER)
    finally:
        driver.quit()
