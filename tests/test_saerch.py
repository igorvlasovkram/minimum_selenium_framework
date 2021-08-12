from minimum_selenium_framework.helpers import own_selene as browser


def test_on_google():
    browser.visit('https://google.com')
    browser.element('[name=q]').should_be_blank()

    browser.element('[name=q]').set_value('yashaka python selene').press_enter()

    browser.should_have_title_containing('yashaka python selene')
