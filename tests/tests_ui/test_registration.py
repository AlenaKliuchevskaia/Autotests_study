import time
import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from faker import Faker

# регистрация с полностью валидными данными
@pytest.mark.ui                  # pytest -m "ui" в консоли запустит тесты ui
@pytest.mark.registration
@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.regression
@allure.description('Регистрация пользователя с полностью валидными данными')
@allure.tag('positive', 'ui', 'regression')
def test_positive_registration(browser, base_url, wait, faker_data):
    browser.get(f'{base_url}/sign_up')
    email_field = wait.until(EC.presence_of_element_located((By.ID, 'email')))
    email_field.send_keys(faker_data.get('email'))
    browser.find_element(By.ID, 'username').send_keys(faker_data.get('name'))
    browser.find_element(By.ID, 'pass1').send_keys(faker_data.get('password'))
    browser.find_element(By.ID, 'pass2').send_keys(faker_data.get('password'))
    browser.find_element(By.CSS_SELECTOR, '.ui.button.blue').click()
    wait.until(EC.url_to_be(f'{base_url}/login'))
    assert browser.current_url == 'http://95.182.122.183:3000/login'
    alert = browser.find_element(By.CSS_SELECTOR, '.Toastify__toast-body')
    assert alert.get_attribute('textContent') == 'Вы успешно зарегистрировались'

# регистрация с доменом ".рф" в электронной почте
@pytest.mark.ui
@pytest.mark.registration
@pytest.mark.smoke
@pytest.mark.negative
@pytest.mark.regression
@allure.description('Регистрация пользователя с доменом ".рф" в электронной почте')
@allure.tag('negative', 'ui', 'regression')
def test_registration_ru_domain(browser, base_url, wait, faker_data):
    browser.get(f'{base_url}/sign_up')
    email_field = wait.until(EC.presence_of_element_located((By.ID, 'email')))
    email_field.send_keys('куликова@муп.рф')
    browser.find_element(By.ID, 'username').send_keys(faker_data.get('name'))
    browser.find_element(By.ID, 'pass1').send_keys(faker_data.get('password'))
    browser.find_element(By.ID, 'pass2').send_keys(faker_data.get('password'))
    browser.find_element(By.CSS_SELECTOR, '.ui.button.blue').click()
    assert browser.current_url == 'http://95.182.122.183:3000/sign_up'
    alert = browser.find_element(By.CSS_SELECTOR, '.mt-2.text-sm.text-rose-600.italic')
    assert alert.get_attribute('textContent') == 'Укажите корректный mail'

# регистрация с паролем менее 8 символов
@pytest.mark.ui
@pytest.mark.registration
@pytest.mark.smoke
@pytest.mark.negative
@pytest.mark.regression
@allure.description('Регистрация пользователя с паролем длиной менее 8 символов')
@allure.tag('negative', 'ui', 'regression')
def test_registration_short_password(browser, base_url, wait, faker_data):
    browser.get(f'{base_url}/sign_up')
    email_field = wait.until(EC.presence_of_element_located((By.ID, 'email')))
    email_field.send_keys(faker_data.get('email'))
    browser.find_element(By.ID, 'username').send_keys(faker_data.get('name'))
    browser.find_element(By.ID, 'pass1').send_keys('123qwer')
    browser.find_element(By.ID, 'pass2').send_keys('123qwer')
    browser.find_element(By.CSS_SELECTOR, '.ui.button.blue').click()
    assert browser.current_url == 'http://95.182.122.183:3000/sign_up'
    alert = browser.find_element(By.CSS_SELECTOR, '.mt-2.text-sm.text-rose-600.italic')
    assert alert.get_attribute('textContent') == 'Не менее 8 символов'

# регистрация с паролем, в котором только цифры
@pytest.mark.ui
@pytest.mark.registration
@pytest.mark.smoke
@pytest.mark.negative
@pytest.mark.regression
@allure.description('Регистрация пользователя с паролем, состоящим из одних цифр')
@allure.tag('negative', 'ui', 'regression')
def test_registration_numeric_password(browser, base_url, wait, faker_data):
    browser.get(f'{base_url}/sign_up')
    email_field = wait.until(EC.presence_of_element_located((By.ID, 'email')))
    email_field.send_keys(faker_data.get('email'))
    browser.find_element(By.ID, 'username').send_keys(faker_data.get('name'))
    browser.find_element(By.ID, 'pass1').send_keys('12345678')
    browser.find_element(By.ID, 'pass2').send_keys('12345678')
    browser.find_element(By.CSS_SELECTOR, '.ui.button.blue').click()
    browser.implicitly_wait(2)
    assert browser.current_url == 'http://95.182.122.183:3000/sign_up'
    alert = browser.find_element(By.CSS_SELECTOR, '.Toastify__toast-body')
    assert alert.get_attribute('textContent') == 'password: This password is entirely numeric.'

# регистрация с паролем, в котором только буквы латинского алфавита
@pytest.mark.ui
@pytest.mark.registration
@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.regression
@allure.description('Регистрация пользователя с паролем, состоящим из одних букв латинского алфавита')
@allure.tag('positive', 'ui', 'regression')
def test_registration_alpha_password(browser, base_url, wait, faker_data):
    browser.get(f'{base_url}/sign_up')
    email_field = wait.until(EC.presence_of_element_located((By.ID, 'email')))
    email_field.send_keys(faker_data.get('email'))
    browser.find_element(By.ID, 'username').send_keys(faker_data.get('name'))
    browser.find_element(By.ID, 'pass1').send_keys('asdfghjk')
    browser.find_element(By.ID, 'pass2').send_keys('asdfghjk')
    browser.find_element(By.CSS_SELECTOR, '.ui.button.blue').click()
    wait.until(EC.url_to_be(f'{base_url}/login'))
    assert browser.current_url == 'http://95.182.122.183:3000/login'
    alert = browser.find_element(By.CSS_SELECTOR, '.Toastify__toast-body')
    assert alert.get_attribute('textContent') == 'Вы успешно зарегистрировались'

# регистрация с паролем, в котором только символы
@pytest.mark.ui
@pytest.mark.registration
@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.regression
@allure.description('Регистрация пользователя с паролем, состоящим из одних символов')
@allure.tag('positive', 'ui', 'regression')
def test_registration_characters_password(browser, base_url, wait, faker_data):
    browser.get(f'{base_url}/sign_up')
    email_field = wait.until(EC.presence_of_element_located((By.ID, 'email')))
    email_field.send_keys(faker_data.get('email'))
    browser.find_element(By.ID, 'username').send_keys(faker_data.get('name'))
    browser.find_element(By.ID, 'pass1').send_keys('!@#$%^&*')
    browser.find_element(By.ID, 'pass2').send_keys('!@#$%^&*')
    browser.find_element(By.CSS_SELECTOR, '.ui.button.blue').click()
    wait.until(EC.url_to_be(f'{base_url}/login'))
    assert browser.current_url == 'http://95.182.122.183:3000/login'
    alert = browser.find_element(By.CSS_SELECTOR, '.Toastify__toast-body')
    assert alert.get_attribute('textContent') == 'Вы успешно зарегистрировались'


# регистрация с паролем, в котором только буквы кириллицы
@pytest.mark.ui
@pytest.mark.registration
@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.regression
@allure.description('Регистрация пользователя с паролем, состоящим из одних букв русского алфавита')
@allure.tag('positive', 'ui', 'regression')
def test_registration_cirillic_password(browser, base_url, wait, faker_data):
    browser.get(f'{base_url}/sign_up')
    email_field = wait.until(EC.presence_of_element_located((By.ID, 'email')))
    email_field.send_keys(faker_data.get('email'))
    browser.find_element(By.ID, 'username').send_keys(faker_data.get('name'))
    browser.find_element(By.ID, 'pass1').send_keys('Абвгдежзи')
    browser.find_element(By.ID, 'pass2').send_keys('Абвгдежзи')
    browser.find_element(By.CSS_SELECTOR, '.ui.button.blue').click()
    wait.until(EC.url_to_be(f'{base_url}/login'))
    assert browser.current_url == 'http://95.182.122.183:3000/login'
    alert = browser.find_element(By.CSS_SELECTOR, '.Toastify__toast-body')
    assert alert.get_attribute('textContent') == 'Вы успешно зарегистрировались'


# пароли при регистрации не совпадают
@pytest.mark.ui
@pytest.mark.registration
@pytest.mark.smoke
@pytest.mark.negative
@pytest.mark.regression
@allure.description('Пароли при регистрации не совпадают')
@allure.tag('negative', 'ui', 'regression')
def test_registration_different_passwords(browser, base_url, wait, faker_data):
    browser.get(f'{base_url}/sign_up')
    email_field = wait.until(EC.presence_of_element_located((By.ID, 'email')))
    email_field.send_keys(faker_data.get('email'))
    browser.find_element(By.ID, 'username').send_keys(faker_data.get('name'))
    browser.find_element(By.ID, 'pass1').send_keys('qwerty789')
    browser.find_element(By.ID, 'pass2').send_keys('qwertyu789')
    browser.find_element(By.CSS_SELECTOR, '.ui.button.blue').click()
    browser.implicitly_wait(2)
    assert browser.current_url == 'http://95.182.122.183:3000/sign_up'
    alert = browser.find_element(By.CSS_SELECTOR, '.mt-2.text-sm.text-rose-600.italic')
    assert alert.get_attribute('textContent') == 'Пароли не совпадают'


# pytest -v -k test_positive_registration --alluredir=allure-results --clean-alluredir

# allure generate allure-results -o allure-report --clean

# allure open allure-report
