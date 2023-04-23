from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from appium.webdriver.common.appiumby import AppiumBy
import pytest


class Login:
    @staticmethod
    def test_login(driver, email, password):
        # login button
        check(driver, 'com.ajaxsystems:id/login').click()
        # email input
        check(driver, 'com.ajaxsystems:id/login').send_keys(email)
        # password input
        check(driver, 'com.ajaxsystems:id/password').send_keys(password)
        # confirm button
        check(driver, 'com.ajaxsystems:id/next').click()
        # alert dismiss
        check(driver, 'com.ajaxsystems:id/cancel_button').click()
        assert 'start managing the security system' in check(driver, 'com.ajaxsystems:id/addFirstHub').text


class Sidebar(Login):
    def test_sidebar(self, driver, email, password):
        # correct login
        self.test_login(driver, email, password)
        # sidebar button
        check(driver, 'com.ajaxsystems:id/menuDrawer').click()
        # check if the sidebar is displayed
        assert check(driver, 'com.ajaxsystems:id/design_navigation_view').is_displayed()
        # check the 'add_hub' button
        add_hub = check(driver, 'com.ajaxsystems:id/addHub')
        assert add_hub.is_displayed() and add_hub.is_enabled()
        # check the 'app_settings' button
        app_settings = check(driver, 'com.ajaxsystems:id/settings')
        assert app_settings.is_displayed() and app_settings.is_enabled()
        # check the 'help' button
        help_ = check(driver, 'com.ajaxsystems:id/help')
        assert help_.is_displayed() and help_.is_enabled()
        # check the 'report' button
        report = check(driver, 'com.ajaxsystems:id/logs')
        assert report.is_displayed() and report.is_enabled()

        driver.quit()


def check(driver, locator):
    return WebDriverWait(driver, 10).until(ec.visibility_of_element_located((AppiumBy.ID, locator)))


users = {
        'user1_correct': ('user_email', 'user_password'),
        'user2_incorrect': ('user_email', 'user_password'),
        'user3_incorrect': ('user_email', 'user_password'),
        'user4_incorrect': ('user_email', 'user_password'),
    }


@pytest.mark.parametrize('email, password', [users.get('user1_correct'), users.get('user2_incorrect'), 
                                             users.get('user3_incorrect'), users.get('user4_incorrect')])
def test_login(driver, email, password):
    login = Login()
    login.test_login(driver, email, password)


@pytest.mark.parametrize('email, password', [users.get('user1_correct')])
def test_sidebar(driver, email, password):
    sidebar = Sidebar()
    sidebar.test_sidebar(driver, email, password)
