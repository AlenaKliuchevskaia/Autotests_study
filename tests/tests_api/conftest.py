import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import requests
from faker import Faker
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


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

@pytest.fixture
def api_url(base_url):
    return f'{base_url}:8000/api/v1'

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

# получаем данные зарегистрированного пользователя
@pytest.fixture
def registered_user(api_url, faker_data):
    user_data = {
        'username': faker_data['name'],
        'email': faker_data['email'],
        'password': faker_data['password']
    }
    response = requests.post(f'{api_url}/users/', json=user_data)
    assert response.status_code == 201
    return user_data

# получаем токен для зарегистрированного пользователя
@pytest.fixture
def auth_token(api_url, registered_user):
    auth_data = {
        'email': registered_user['email'],
        'password': registered_user['password']
    }
    response = requests.post(f'{api_url}/jwt/create/', json=auth_data)
    assert response.status_code == 200
    return response.json()['access']

# получаем заголовки с токеном для авторизованных запросов
@pytest.fixture
def auth_headers(auth_token):
    return {'Authorization': f'Bearer {auth_token}'}