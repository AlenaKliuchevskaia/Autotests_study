import pytest
import requests
import allure

# выход пользователя из системы
@allure.description('Выход пользователя из системы')
@allure.tag('positive', 'api', 'regression')
@pytest.mark.user_logout
def test_user_logout(api_url, auth_headers):
    response = requests.get(f'{api_url}/users/logout/', headers=auth_headers)
    assert response.status_code == 200
    assert response.json()['message'] == 'Вы разлогинены.'
