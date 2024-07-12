import pytest
from tests.data import payloads as p
from endpoints.post_authorization import CreateToken
from endpoints.get_token_status import CheckTokenStatus


@pytest.fixture()
def user_token():
    old_token = CheckTokenStatus
    token = old_token.check_token_status()
    created_token = CreateToken()
    created_token.create_token(p.token_payload)
    return created_token.token


@pytest.fixture()
def created_token():
    return CreateToken()

@pytest.fixture()
def checked_token():
    return CheckTokenStatus()
