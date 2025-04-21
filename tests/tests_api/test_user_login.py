import pytest
import requests
import allure


def test_login_by_token(auth_token, api_url):
    user_data = {
        'token': auth_token
    }
    response = requests.post(f'{api_url}/jwt/verify/', json=user_data)
    assert response.status_code == 200