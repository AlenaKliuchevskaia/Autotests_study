import time

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from faker import Faker


@pytest.mark.ui                  # pytest -m "ui" в консоли запустит тесты ui
@pytest.mark.registration
@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.regression
def test_positive_registration(browser, base_url, wait, faker_data):
    browser.get(f'{base_url}/sign_up')
    email_field = wait.until(EC.presence_of_element_located((By.ID, 'email')))
    email_field.send_keys(faker_data.get('email'))
    browser.find_element(By.ID, 'name').send_keys(faker_data.get('name'))
    browser.find_element(By.ID, 'pass1').send_keys(faker_data.get('password'))
    browser.find_element(By.ID, 'pass2').send_keys(faker_data.get('password'))
    browser.find_element(By.CSS_SELECTOR, '.ui.button.blue').click()
    wait.until(EC.url_to_be(f'{base_url}/login'))
    assert browser.current_url == 'http://95.182.122.183/login'
    alert = browser.find_element(By.CSS_SELECTOR, '.Toastify__toast-body')
    assert alert.get_attribute('textContent') == 'Вы успешно зарегистрировались'


# pytest -v -k test_positive_registration --alluredir=allure-results --clean-alluredir

# allure generate allure-results -o allure-report --clean

# allure open allure-report
