from appium import webdriver
import subprocess
import pytest


def udid():
    output = subprocess.check_output(['adb', 'devices'])
    devices = output.decode().strip().split('\n')
    devices = [device.split('\t')[0] for device in devices]
    return devices[1]


@pytest.fixture
def driver():
    desired_caps = {
        'autoGrantPermissions': True,
        'deviceName': 'Pixel 2 API 30',
        'platformName': 'Android',
        'version': '11.0',
        'udid': udid(),
        'appPackage': 'com.ajaxsystems',
        'appWaitActivity': 'com.ajaxsystems.ui.activity.HelloActivity',
        'app': 'ajax.apk' # You need to download ajax.apk to the root directory
    }
    return webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
