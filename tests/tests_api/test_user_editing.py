import pytest
import requests
import allure

# получение данных существующего пользователя
@allure.description('Получение данных существующего пользователя')
@allure.tag('positive', 'api', 'regression')
@pytest.mark.user_me
def test_users_read(auth_headers, api_url):
    response = requests.get(f'{api_url}/users/me/', headers=auth_headers)
    assert response.status_code == 200
    assert 'username' in response.json()
    assert 'id' in response.json()
    assert 'email' in response.json()

# редактирование имени пользователя
@allure.description('Редактирование имени пользователя')
@allure.tag('positive', 'api', 'regression')
@pytest.mark.user_update
def test_username_edit(auth_headers, api_url):
    new_name = {
        'username': 'Карина'
    }
    response = requests.patch(f'{api_url}/users/me/', headers=auth_headers, json=new_name)
    assert response.status_code == 200
    assert 'username' in response.json()
    assert 'id' in response.json()
    assert 'email' in response.json()
    assert response.json()['username'] == new_name['username']

# удаление пользователя
@allure.description('Удаление пользователя')
@allure.tag('positive', 'api', 'regression')
@pytest.mark.user_delete
def test_delete_user(auth_headers, api_url, registered_user):
    password = {
        'current_password': registered_user['password']
    }
    response = requests.delete(f'{api_url}/users/me/', headers=auth_headers, json=password)
    assert response.status_code == 204

# восстановление пароля
@allure.description('Восстановление пароля')
@allure.tag('positive', 'api', 'regression')
@pytest.mark.password_restore
def test_restore_password(api_url, registered_user):
    email = {
        'email': registered_user['email']
    }
    response = requests.post(f'{api_url}/users/restore/', json=email)
    assert response.status_code == 201

# изменение пароля
@pytest.mark.password_change
@allure.description('Изменение пароля')
@allure.tag('positive', 'api', 'regression')
def test_edit_password(api_url, auth_headers, registered_user):
    new_password = {
        'new_password': 'string123Y',
        'current_password': registered_user['password']
    }
    response = requests.post(f'{api_url}/users/set_password/', json=new_password, headers=auth_headers)
    assert response.status_code == 201
