import pytest
from tests.data import payloads as p
from endpoints.post_authorization import CreateToken
from endpoints.get_token_status import CheckTokenStatus
from endpoints.get_memes import MemesFetcher
from endpoints.get_meme_by_id import SingleMemeFetcher
from endpoints.create_new_meme import MemeCreator
from endpoints.delete_meme_by_id import MemeAnnihilator
from endpoints.change_meme import MemeChanger


@pytest.fixture()
def user_token(checked_token, created_token):
    token = checked_token.active_token()
    checked_token.check_token_status(token)
    if checked_token.response.status_code != 200 or 'Token is alive' not in checked_token.response.text:
        created_token.create_token(p.token_payload)
        created_token.update_token_in_file()
        token = created_token.token
    return token


@pytest.fixture()
def another_user_token(created_token):
    created_token.create_token(p.another_token_payload)
    token = created_token.token
    return token


@pytest.fixture()
def meme_id(creating_meme, deleting_meme, user_token):
    header = creating_meme.auth_header(user_token)
    meme_id = creating_meme.create_meme(header, p.meme_payload.copy())
    yield meme_id
    deleting_meme.delete_meme(header, meme_id)


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


@pytest.fixture()
def creating_meme():
    return MemeCreator()


@pytest.fixture()
def deleting_meme():
    return MemeAnnihilator()


@pytest.fixture()
def change_meme():
    return MemeChanger()
