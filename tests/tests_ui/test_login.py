# kulikova@ngs.ru 1234qwerty
# куликова@муп.рф :?*гшщз
import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import allure

# Вход зарегистрированного пользователя
@pytest.mark.ui
@pytest.mark.login
@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.regression
@allure.description('Вход зарегистрированного пользователя')
@allure.tag('positive', 'ui', 'regression')
def test_positive_login(browser, base_url, wait):
    browser.get(f'{base_url}/login')
    email_field = wait.until(EC.presence_of_element_located((By.ID, 'email')))
    email_field.send_keys('kulikova@ngs.ru')
    browser.find_element(By.ID, 'password').send_keys('1234qwerty')
    browser.find_element(By.CSS_SELECTOR, '.ui.button.blue').click()
    wait.until(EC.url_to_be(f'{base_url}/home'))
    assert browser.current_url == 'http://95.182.122.183:3000/home'


# Вход зарегистрированного пользователя с неверным логином
@pytest.mark.ui
@pytest.mark.login
@pytest.mark.smoke
@pytest.mark.negative
@pytest.mark.regression
@allure.description('Вход зарегистрированного пользователя с неверным логином')
@allure.tag('negative', 'ui', 'regression')
def test_incorrect_login(browser, base_url, wait):
    browser.get(f'{base_url}/login')
    email_field = wait.until(EC.presence_of_element_located((By.ID, 'email')))
    email_field.send_keys('a')
    browser.find_element(By.ID, 'password').send_keys('1234qwerty')
    browser.find_element(By.CSS_SELECTOR, '.ui.button.blue').click()
    assert browser.current_url == 'http://95.182.122.183:3000/login'
    browser.implicitly_wait(2)
    alert = browser.find_element(By.CSS_SELECTOR, '.Toastify__toast-body')
    assert alert.get_attribute('textContent') == 'No active account found with the given credentials'


# Вход зарегистрированного пользователя с неверным паролем
@pytest.mark.ui
@pytest.mark.login
@pytest.mark.smoke
@pytest.mark.negative
@pytest.mark.regression
@allure.description('Вход зарегистрированного пользователя с неверным паролем')
@allure.tag('negative', 'ui', 'regression')
def test_incorrect_password(browser, base_url, wait):
    browser.get(f'{base_url}/login')
    email_field = wait.until(EC.presence_of_element_located((By.ID, 'email')))
    email_field.send_keys('kulikova@ngs.ru')
    browser.find_element(By.ID, 'password').send_keys('1234')
    browser.find_element(By.CSS_SELECTOR, '.ui.button.blue').click()
    assert browser.current_url == 'http://95.182.122.183:3000/login'
    browser.implicitly_wait(2)
    alert = browser.find_element(By.CSS_SELECTOR, '.Toastify__toast-body')
    assert alert.get_attribute('textContent') == 'No active account found with the given credentials'
