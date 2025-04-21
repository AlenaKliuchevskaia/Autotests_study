import time

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from faker import Faker



@pytest.fixture
def faker_data():
    fake = Faker('ru_Ru')
    return {
        "email": fake.ascii_free_email(),
        "name": fake.first_name(),
        "password": fake.password(length=8)
    }


# url = 'http://95.182.122.183/sign_up'

@pytest.fixture
def browser():
    driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    # драйвер выполнил тест
    yield driver
    driver.quit()

@pytest.fixture
def base_url():
    return 'http://95.182.122.183'

@pytest.fixture(params=[
    {"email": "17userMonday@mail.ru",
    "password": "qwertyui1",
    "name": "user56"},
    {"email": "18userMonday@mail.ru",
    "password": "qwertyui12",
    "name": "user56"},
    {"email": "19userMonday@mail.ru",
    "password": "qwertyui123",
    "name": "user56"}
])
def registration_data(request):
    return request.param

@pytest.fixture
def wait(browser):
    return WebDriverWait(browser, 10)

@pytest.mark.ui                  # pytest -m "ui" в консоли запустит тесты ui
@pytest.mark.registration
@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.regression
def test_positive_registration(browser, base_url, wait, faker_data):
    #driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    browser.get(f'{base_url}/sign_up')
    email_field = wait.until(EC.presence_of_element_located((By.ID, 'email')))
    email_field.send_keys(faker_data.get('email'))
    browser.find_element(By.ID, 'name').send_keys(faker_data.get('name'))
    #browser.find_element(By.ID, 'email').send_keys('14userMonday@mail.ru')
    browser.find_element(By.ID, 'pass1').send_keys(faker_data.get('password'))
    browser.find_element(By.ID, 'pass2').send_keys(faker_data.get('password'))
    browser.find_element(By.CSS_SELECTOR, '.ui.button.blue').click()
    #time.sleep(5)
    wait.until(EC.url_to_be(f'{base_url}/login'))
    assert browser.current_url == 'http://95.182.122.183/login'
    alert = browser.find_element(By.CSS_SELECTOR, '.Toastify__toast-body')
    assert alert.get_attribute('textContent') == 'Вы успешно зарегистрировались'
    #driver.quit()


