import pytest
from tests.data import payloads as p
from endpoints.post_authorization import CreateToken
from endpoints.get_token_status import CheckTokenStatus
from endpoints.get_memes import MemesFetcher
from endpoints.get_meme_by_id import SingleMemeFetcher


@pytest.fixture()  # autouse=True
def user_token(checked_token, created_token):
    token = checked_token.active_token()
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

@pytest.fixture()
def fetch_all_memes():
    return MemesFetcher()

@pytest.fixture()
def fetch_meme():
    return SingleMemeFetcher()
