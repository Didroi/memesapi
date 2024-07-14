import pytest
import requests
from tests.data import payloads as p
from endpoints.post_authorization import CreateToken
from endpoints.get_token_status import CheckTokenStatus
from tests.data import token as t
from tests.data import headers as h
from tests.data import url

@pytest.fixture()
def user_token():
    token = t.token
    headers = h.non_auth_header
    response = requests.get(
        f'{url.url}/authorize/{token}',
        headers=headers
    )

    if response.status_code != 200 or 'Token is alive' not in response.text:
        token_creation = CreateToken()
        token_creation.create_token(p.token_payload)
        token = token_creation.response.json()['token']
        with open('data/token.py', 'w') as f:
            f.write(f'token = "{token}"')
    return token

@pytest.fixture()
def created_token():
    return CreateToken()

@pytest.fixture()
def checked_token():
    return CheckTokenStatus()
