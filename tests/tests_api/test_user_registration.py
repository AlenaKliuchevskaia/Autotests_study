import pytest
import requests
import allure

# регистрация нового пользователя
@allure.description('Регистрация нового пользователя')
@allure.tag('positive', 'api', 'regression')
@pytest.mark.user_registration
def test_user_registration(api_url, faker_data):
    user_data = {
        'username': faker_data['name'],
        'email': faker_data['email'],
        'password': faker_data['password']
    }
    response = requests.post(f'{api_url}/users/', json=user_data)

    assert response.status_code == 201
    assert 'id' in response.json()
    assert response.json()['username'] == user_data['username']
    assert response.json()['email'] == user_data['email']


# регистрация username 1 символ
@allure.description('Регистрация нового пользователя с username длиной 1 символ')
@allure.tag('positive', 'api', 'regression')
@pytest.mark.user_registration
def test_username_min_length(api_url, faker_data):
    user_data = {
        'username': 'a',
        'email': faker_data['email'],
        'password': faker_data['password']
    }
    response = requests.post(f'{api_url}/users/', json=user_data)

    assert response.status_code == 201
    assert response.json()['username'] == user_data['username']
    assert response.json()['email'] == user_data['email']


# регистрация username 255 символов
@allure.description('Регистрация нового пользователя с username длиной 255 символов')
@allure.tag('positive', 'api', 'regression')
@pytest.mark.user_registration
def test_username_max_length(api_url, faker_data):
    long_username = 'a' * 255
    user_data = {
        'username': long_username,
        'email': faker_data['email'],
        'password': faker_data['password']
    }
    response = requests.post(f'{api_url}/users/', json=user_data)

    assert response.status_code == 201
    assert response.json()['username'] == user_data['username']

# регистрация username 256 символов
@allure.description('Регистрация нового пользователя с username, превышающим допустимую длину')
@allure.tag('negative', 'api', 'regression')
@pytest.mark.user_registration
def test_username_exceeds_max_length(api_url, faker_data):
    long_username = 'b' * 256
    user_data = {
        'username': long_username,
        'email': faker_data['email'],
        'password': faker_data['password']
    }
    response = requests.post(f'{api_url}/users/', json=user_data)

    assert response.status_code == 400
    assert 'username' in response.json()
    assert response.json()['username'][0] == 'Ensure this field has no more than 255 characters.'

# Регистрация пользователя с минимальной длиной email
@allure.description('Регистрация пользователя с минимальной длиной email')
@allure.tag('positive', 'api', 'regression')
@pytest.mark.user_registration
def test_email_min_length(api_url, faker_data):
    min_email = 'k@hey.com'
    user_data = {
        'username': faker_data['name'],
        'email': min_email,
        'password': faker_data['password']
    }
    response = requests.post(f'{api_url}/users/', json=user_data)

    assert response.status_code == 201
    assert response.json()['email'] == user_data['email']

# регистрация с email максимальной длины
@allure.description('Регистрация пользователя с максимальной длиной email')
@allure.tag('positive', 'api', 'regression')
@pytest.mark.user_registration
def test_email_max_length(api_url, faker_data):
    max_email = 'qwertyuioplkjhgfdsazxcvbnmpoiuy67t_hgfdsaw@hey.com'
    user_data = {
        'username': faker_data['name'],
        'email': max_email,
        'password': faker_data['password']
    }
    response = requests.post(f'{api_url}/users/', json=user_data)

    assert response.status_code == 201
    assert response.json()['email'] == user_data['email']

# регистрация с emal, превышающим максимальную длину
@allure.description('Регистрация пользователя с email, превышающим максимальную длину')
@allure.tag('negative', 'api', 'regression')
@pytest.mark.user_registration
def test_email_exceeds_max_length(api_url, faker_data):
    long_email = 'qweUrtyuioplkjhgfdsazxcvbnmpoiuy67t_hgfdsaw@hey.com'
    user_data = {
        'username': faker_data['name'],
        'email': long_email,
        'password': faker_data['password']
    }
    response = requests.post(f'{api_url}/users/', json=user_data)

    assert response.status_code == 400
    assert 'email' in response.json()
    assert response.json()['email'][0] == 'Ensure this field has no more than 50 characters.'

# регистрация с паролем минимальной длины
@allure.description('Регистрация пользователя с паролем минимальной длины')
@allure.tag('positive', 'api', 'regression')
@pytest.mark.user_registration
def test_min_password(api_url, faker_data):
    min_password = 'a1Njkop3'   # минимальная длина пароля 8 символов
    user_data = {
        'username': faker_data['name'],
        'email': faker_data['email'],
        'password': min_password
    }
    response = requests.post(f'{api_url}/users/', json=user_data)

    assert response.status_code == 201
    assert response.json()['password'] == user_data['password']

# регистрация с паролем меньше минимальной длины
@allure.description('Регистрация пользователя с паролем меньше минимальной длины')
@allure.tag('negative', 'api', 'regression')
@pytest.mark.user_registration
def test_small_password(api_url, faker_data):
    small_password = '9hgT7mn'
    user_data = {
        'username': faker_data['name'],
        'email': faker_data['email'],
        'password': small_password
    }
    response = requests.post(f'{api_url}/users/', json=user_data)

    assert response.status_code == 400
    assert response.json()['password'][0] == 'This password is too short. It must contain at least 8 characters.'

# регистрация с пустым паролем
@allure.description('Регистрация пользователя с незаполненным полем пароля')
@allure.tag('negative', 'api', 'regression')
@pytest.mark.user_registration
def test_empty_password(api_url, faker_data):
    empty_password = ''
    user_data = {
        'username': faker_data['name'],
        'email': faker_data['email'],
        'password': empty_password
    }
    response = requests.post(f'{api_url}/users/', json=user_data)

    assert response.status_code == 400
    assert response.json()['password'][0] == 'This field may not be blank.'
