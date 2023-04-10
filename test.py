from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy
import pytest


class TestAjax:
    users = {
        'correct_user': ('qa.********.automation@gmail.com', 'qa_automation**********'),
        'incorrect_user': ('test@ukr.net', 'test12345')
    }

    @staticmethod
    def log(driver):
        with open('ajax_test.log', 'a', encoding='utf-8') as file:
            logs = driver.get_log('logcat')
            for log in logs:
                file.write(str(log) + '\n')

    @staticmethod
    def check(driver, locator):
        return WebDriverWait(driver, 10).until(EC.visibility_of_element_located((AppiumBy.ID, locator)))

    @pytest.mark.parametrize('email_, password_', [users.get('correct_user'), users.get('incorrect_user')])
    def test_login(self, driver, email_, password_):
        # login button
        self.check(driver, 'com.ajaxsystems:id/login').click()
        # email input
        self.check(driver, 'com.ajaxsystems:id/login').send_keys(email_)
        # password input
        self.check(driver, 'com.ajaxsystems:id/password').send_keys(password_)
        # confirm button
        self.check(driver, 'com.ajaxsystems:id/next').click()
        # alert dismiss
        self.check(driver, 'com.ajaxsystems:id/cancel_button').click()
        assert 'start managing the security system' in self.check(driver, 'com.ajaxsystems:id/addFirstHub').text

        self.log(driver)

    def test_sidebar(self, driver):
        # correct login
        self.test_login(driver, 'qa.********.automation@gmail.com', 'qa_automation**********')
        # sidebar button
        self.check(driver, 'com.ajaxsystems:id/menuDrawer').click()
        # check if the sidebar is displayed
        assert self.check(driver, 'com.ajaxsystems:id/design_navigation_view').is_displayed()
        # check the 'add_hub' button
        add_hub = self.check(driver, 'com.ajaxsystems:id/addHub')
        assert add_hub.is_displayed() and add_hub.is_enabled()
        # check the 'app_settings' button
        app_settings = self.check(driver, 'com.ajaxsystems:id/settings')
        assert app_settings.is_displayed() and app_settings.is_enabled()
        # check the 'help' button
        help_ = self.check(driver, 'com.ajaxsystems:id/help')
        assert help_.is_displayed() and help_.is_enabled()
        # check the 'report' button
        report = self.check(driver, 'com.ajaxsystems:id/logs')
        assert report.is_displayed() and report.is_enabled()

        self.log(driver)
        driver.quit()
