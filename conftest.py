import pytest
from tests.data import payloads as p
from endpoints.post_authorization import CreateToken
from endpoints.get_token_status import CheckTokenStatus
from tests.data import token as t


@pytest.fixture()
def user_token(checked_token, created_token):
    token = t.tokens['active token']
    checked_token.check_token_status(token)

    if checked_token.response.status_code != 200 or 'Token is alive' not in checked_token.response.text:
        created_token.create_token(p.token_payload)
        created_token.update_token_in_file()
        token = created_token.token

    return token

@pytest.fixture()
def created_token():
    return CreateToken()

@pytest.fixture()
def checked_token():
    return CheckTokenStatus()

