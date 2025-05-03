import os
import time

import allure
import pytest
from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from faker import Faker


SCREENSHOTS_DIR = os.path.join('screenshots')

@pytest.fixture
def faker_data():
    fake = Faker('ru_Ru')
    return {
        "email": fake.ascii_free_email(),
        "name": fake.first_name(),
        "password": fake.password(length=8)
    }

@pytest.fixture
def browser(request):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    request.node.driver = driver
    yield driver
    driver.quit()


@pytest.fixture
def base_url():
    return 'http://95.182.122.183:3000'

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

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == 'call' and rep.failed:                                  # когда тест работает и он упал
        driver = getattr(item._request.node, 'driver', None)
        if driver:
            os.makedirs(SCREENSHOTS_DIR, exist_ok=True)                   # создание директории со скриншотами, если ее нет
            timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")                # используем дату и время для названия скриншота
            screenshot_path = os.path.join(SCREENSHOTS_DIR, f"screenshot_{timestamp}.png")

            driver.save_screenshot(screenshot_path)

            # allure.attach(driver.get_screenshot_as_png(),
            #               name="screenshot",
            #               attachment_type=allure.attachment_type.PNG)
            with open(screenshot_path, "rb") as image_file:
                allure.attach(image_file.read(), name=f"Screenshot {timestamp}", attachment_type=AttachmentType.PNG)


# удалить старые скриншоты
@pytest.fixture(scope="session", autouse=True)
def clean_screenshots_before_tests():
    if os.path.exists(SCREENSHOTS_DIR):
        for filename in os.listdir(SCREENSHOTS_DIR):
            file_path = os.path.join(SCREENSHOTS_DIR, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"не удалить файл {file_path}: {e}")
    else:
        os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
