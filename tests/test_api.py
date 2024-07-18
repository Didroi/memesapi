import pytest
import allure
from tests.data import payloads as p
from tests.data import token as t


user = p.token_payload['name']
auth_payload = p.token_payload.copy()
obs_token = t.tokens['obsolete token']


@allure.description('Creating new token for user')
@allure.feature('Authorization')
@allure.story('01. Create token')
@allure.title('POST /authorize')
@pytest.mark.regression
@pytest.mark.smoke
def test_create_token(created_token):
    created_token.create_token(auth_payload)
    assert created_token.check_status_is_(200)
    assert created_token.check_response_user_is_(user)
    assert created_token.check_response_has_token()


@allure.description('Performance test emulation with only 2 tries')  # In real Test we can use bigger count
@allure.feature('Authorization')
@allure.story('02. Many tries')
@allure.title('POST /authorize')
@pytest.mark.regression
def test_multi_create_token(created_token):
    for _ in range(2):
        created_token.create_token(auth_payload)
        assert created_token.check_status_is_(200)
        assert created_token.check_response_user_is_(user)
        assert created_token.check_response_has_token()


@allure.description('Check incorrect strings in name')
@allure.feature('Authorization')
@allure.story('03. Incorrect user names')
@allure.title('POST /authorize')
@pytest.mark.parametrize('name', [
    '', ' ', '-', "Dima' -", "< ", '/Dima', ' Dima', '$ Pytest',
    'ДмитрийКиселев', 'DoctorAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
    "O'Connor", "Jane!@#", "Štěpán"
])
@pytest.mark.regression
def test_create_token_with_incorrect_name(created_token, name):
    auth_payload['name'] = name
    created_token.create_token(auth_payload)
    assert created_token.check_status_is_(200)
    assert created_token.check_response_user_is_(name)


@allure.description('Check token creation with incorrect type od data')
@allure.feature('Authorization')
@allure.story('04. Incorrect create token')
@allure.title('Negative POST /authorize')
@pytest.mark.parametrize('name', [10, False, ('Dima', ), {}, None])
@pytest.mark.regression
def test_create_incorrect_token(created_token, name):
    auth_payload['name'] = name
    created_token.false_create_token(auth_payload)
    assert created_token.check_status_is_(400)


@allure.description('Check token creation url with another methods')
@allure.feature('Authorization')
@allure.story('05. Wrong authorization')
@allure.title('non-POST /authorize')
@pytest.mark.parametrize('method', ['GET', 'PATCH', 'PUT', 'DELETE'])
@pytest.mark.regression
def test_wrong_authorization_url(created_token, method):
    created_token.wrong_method(auth_payload, method)
    assert created_token.check_status_is_(405)


@allure.description('Check 404 for incorrect curl')
@allure.feature('Authorization')
@allure.story('06. Wrong authorization')
@allure.title('incorrect curl')
@pytest.mark.regression
def test_wrong_authorization_curl(created_token):
    created_token.wrong_url(auth_payload)
    assert created_token.check_status_is_(404)


@allure.description('Check token status')
@allure.feature('Authorization')
@allure.story('07. Check token')
@allure.title('GET /authorize/token')
@pytest.mark.regression
@pytest.mark.smoke
def test_token(user_token, checked_token):
    checked_token.check_token_status(user_token)
    assert checked_token.check_status_is_(200)
    assert checked_token.check_correct_text_in_request()
    assert checked_token.check_user_is_correct(user)

@allure.description('Check incorrect token')
@allure.feature('Authorization')
@allure.story('08. Check incorrect token')
@allure.title('GET /authorize/incorrect token')
@pytest.mark.regression
def test_incorrect_token(checked_token):
    checked_token.check_incorrect_token_status()
    assert checked_token.check_status_is_(404)

@allure.description('Check token with wrong methods')
@allure.feature('Authorization')
@allure.story('09. Wrong token check')
@allure.title('non-GET /authorize/token')
@pytest.mark.parametrize('method', ['POST', 'PATCH', 'PUT', 'DELETE'])
@pytest.mark.regression
def test_wrong_checking_token_url(checked_token, user_token, method):
    checked_token.wrong_method(method, user_token)
    assert checked_token.check_status_is_(405)

@allure.description('Check obsolete token')
@allure.feature('Authorization')
@allure.story('10. Check obsolete token')
@allure.title('GET /authorize/obsolete token')
@pytest.mark.regression
def test_obsolete_token(checked_token):
    checked_token.check_obsolete_token(obs_token)
    assert checked_token.check_status_is_(404)

@allure.description('Check token with wrong url')
@allure.feature('Authorization')
@allure.story('11. Check token with wrong url')
@allure.title('GET /wrong url/token')
@pytest.mark.regression
def test_token_with_wrong_url(user_token, checked_token):
    checked_token.check_token_with_wrong_url(user_token)
    assert checked_token.check_status_is_(404)

@allure.description('Fetch all memes')
@allure.feature('Get Memes')
@allure.story('12. Get memes')
@allure.title('GET /meme')
@pytest.mark.regression
@pytest.mark.smoke
def test_get_memes(user_token, fetch_all_memes):
    fetch_all_memes.fetch_all_memes()
    assert fetch_all_memes.check_status_is_(200)
    assert fetch_all_memes.check_data_is_not_empty()
    assert fetch_all_memes.check_unique_ids()
    # need to add paydentic for check respons structure

@allure.description('Fetch memes without token')
@allure.feature('Get Memes')
@allure.story('13. Wrong get memes')
@allure.title('GET /meme without token')
@pytest.mark.regression
def test_get_memes_without_token(fetch_all_memes):
    fetch_all_memes.fetch_memes_without_token()
    assert fetch_all_memes.check_status_is_(401)

