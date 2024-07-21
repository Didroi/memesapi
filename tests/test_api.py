import pytest
import allure
from tests.data import payloads as p
from endpoints.base_api import BaseApi


user = p.token_payload['name']
auth_payload = p.token_payload.copy()
meme_creation_payload = p.meme_payload.copy()
obs_token = BaseApi.obsolete_token


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


@allure.description('Performance test emulation with only 2 tries. You can use more tries')
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
    header = fetch_all_memes.auth_header(user_token)
    fetch_all_memes.fetch_all_memes(header)
    assert fetch_all_memes.check_status_is_(200)
    assert fetch_all_memes.check_data_is_not_empty()
    assert fetch_all_memes.check_unique_ids()
    # need to add paydentic for check response structure


@allure.description('Fetch memes without token')
@allure.feature('Get Memes')
@allure.story('13. Wrong get memes without token')
@allure.title('GET /meme without token')
@pytest.mark.regression
def test_get_memes_without_token(fetch_all_memes):
    fetch_all_memes.fetch_memes_without_token()
    assert fetch_all_memes.check_status_is_(401)


@allure.description('Fetch memes with incorrect tokens')
@allure.feature('Get Memes')
@allure.story('14. Wrong get memes with incorrect tokens')
@allure.title('GET /meme with incorrect token')
@pytest.mark.parametrize('token', ['token', obs_token, "tok', 'key': 'value'"])  # добавить ' ' (пробел)
@pytest.mark.regression
def test_get_memes_with_incorrect_token(fetch_all_memes, token):
    fetch_all_memes.fetch_memes_with_incorrect_token(token)
    assert fetch_all_memes.check_status_is_(401)
    assert fetch_all_memes.check_sending_token_is_right(token)
    # space in token response with 500 - need new test or correct api and adding in this text


@allure.description('Check memes with wrong methods')
@allure.feature('Get Memes')
@allure.story('15. Wrong methods for getting memes')
@allure.title('non-GET /meme')
@pytest.mark.parametrize('method', ['PATCH', 'PUT', 'DELETE'])
@pytest.mark.regression
def test_wrong_methods_for_getting_memes(fetch_all_memes, user_token, method):
    fetch_all_memes.wrong_method(method, user_token)
    assert fetch_all_memes.check_status_is_(405)


@allure.description('Check single meme by ID')
@allure.feature('Get Memes')
@allure.story('16. Get mem by ID')
@allure.title('GET /meme/id')
@pytest.mark.smoke
@pytest.mark.regression
def test_get_meme_by_id(fetch_meme, user_token, meme_id):
    header = fetch_meme.auth_header(user_token)
    fetch_meme.fetch_meme_by_id(header, meme_id)
    assert fetch_meme.check_status_is_(200)
    assert fetch_meme.check_correct_id_in_response(meme_id)
    # need to add paydentic for check response structure


@allure.description('Check single meme by incorrect ID')
@allure.feature('Get Memes')
@allure.story('17. Get meme by incorrect ID')
@allure.title('GET /meme/incorrect id')
@pytest.mark.parametrize('id', [2, 0, '', ' ', -1, '01', 'a', '*', 1.5])
@pytest.mark.regression
def test_get_meme_by_incorrect_id(fetch_meme, user_token, id):
    header = fetch_meme.auth_header(user_token)
    fetch_meme.fetch_meme_by_id_without_json(header, id)
    assert fetch_meme.check_status_is_(404)

@allure.description('Check single meme without token')
@allure.feature('Get Memes')
@allure.story('18. Get meme without token')
@allure.title('GET /meme/id')
@pytest.mark.regression
def test_get_meme_without_token(fetch_meme, meme_id):
    header = fetch_meme.non_auth_header
    fetch_meme.fetch_meme_by_id_without_json(header, meme_id)
    assert fetch_meme.check_status_is_(401)

@allure.description('Check single meme by ID with incorrect token')
@allure.feature('Get Memes')
@allure.story('19. Get meme by ID with incorrect token')
@allure.title('GET /meme/id')
@pytest.mark.parametrize('token', ['1', 'token', obs_token])  # , '', ' ' добавить пустую строку и пробед (они пятисотят почему-то
@pytest.mark.regression
def test_get_meme_with_incorrect_token(fetch_meme, token, meme_id):
    header = fetch_meme.auth_header(token)
    fetch_meme.fetch_meme_by_id_without_json(header, meme_id)
    assert fetch_meme.check_status_is_(401)

@allure.description('Check single meme with incorrect method')
@allure.feature('Get Memes')
@allure.story('20. Wrong methods for getting single meme by ID')
@allure.title('non-GET /meme/id')
@pytest.mark.parametrize('method', ['POST', 'PATCH'])
@pytest.mark.regression
def test_get_meme_with_incorrect_method(fetch_meme, user_token, meme_id, method):
    header = fetch_meme.auth_header(user_token)
    fetch_meme.fetch_meme_with_incorrect_method(header, meme_id, method)
    assert fetch_meme.check_status_is_(405)

@allure.description('Creating new meme')
@allure.feature('Create Memes')
@allure.story('22. Meme creation')
@allure.title('POST /meme')
@pytest.mark.smoke
@pytest.mark.regression
def test_creation_meme(creating_meme, user_token):
    header = creating_meme.auth_header(user_token)
    creating_meme.create_meme(header, meme_creation_payload)
    assert creating_meme.check_status_is_(200)
    assert creating_meme.check_id_in_response()
    creating_meme.delete_meme_after_creating()
    # need to add paydentic for check response structure

def test_deletion_meme(deleting_meme, user_token, meme_id):
    header = deleting_meme.auth_header(user_token)
    deleting_meme.delete_meme(header, meme_id)
