import pytest
import allure
from tests.data import payloads as p
from endpoints.base_api import BaseApi

auth_payload = p.token_payload
meme_creation_payload = p.meme_payload.copy()
part_of_payload = p.empty_meme_payload.copy()
new_meme_payload = p.new_meme_payload.copy()
pwf = p.payload_without_field
obs_token = BaseApi.obsolete_token
user = p.token_payload['name']


@allure.description('Creating new token for user')
@allure.feature('a. Authorization')
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
@allure.feature('a. Authorization')
@allure.story('02. Many tries of creation')
@allure.title('POST /authorize')
@pytest.mark.regression
def test_multi_create_token(created_token):
    for _ in range(2):
        created_token.create_token(auth_payload)
        assert created_token.check_status_is_(200)
        assert created_token.check_response_user_is_(user)
        assert created_token.check_response_has_token()


@allure.description('Check incorrect strings in name')
@allure.feature('a. Authorization')
@allure.story('03. Create with incorrect user names')
@allure.title('POST /authorize')
@pytest.mark.parametrize('name', [
    '', ' ', '-', "Dima' -", "< ", '/Dima', ' Dima', '$ Pytest',
    'ДмитрийКиселев', 'DoctorAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
    "O'Connor", "Jane!@#", "Štěpán"
])
@pytest.mark.regression
def test_create_token_with_incorrect_name(created_token, name):
    payload = auth_payload.copy()
    payload['name'] = name
    created_token.create_token(payload)
    assert created_token.check_status_is_(200)
    assert created_token.check_response_user_is_(name)


@allure.description('Check token creation with incorrect type od data')
@allure.feature('a. Authorization')
@allure.story('04. Create with incorrect create token')
@allure.title('Negative POST /authorize')
@pytest.mark.parametrize('name', [10, False, ('Dima', ), {}, None])
@pytest.mark.regression
def test_create_incorrect_token(created_token, name):
    payload = auth_payload.copy()
    payload['name'] = name
    created_token.false_create_token(payload)
    assert created_token.check_status_is_(400)


@allure.description('Check token creation url with another methods')
@allure.feature('a. Authorization')
@allure.story('05. Wrong authorization')
@allure.title('non-POST /authorize')
# @pytest.mark.parametrize('method', ['GET'])
# @pytest.mark.parametrize('method', ['DELETE', 'PUT'])  # Был какой-то глюк апишки и тест фейлился в один день
@pytest.mark.parametrize('method', ['GET', 'PATCH', 'PUT', 'DELETE'])
@pytest.mark.regression
def test_wrong_authorization_url(created_token, method):
    created_token.wrong_method(auth_payload, method)
    assert created_token.check_status_is_(405)


@allure.description('Check 404 for incorrect curl')
@allure.feature('a. Authorization')
@allure.story('06. Wrong authorization')
@allure.title('incorrect curl')
@pytest.mark.regression
def test_wrong_authorization_curl(created_token):
    created_token.wrong_url(auth_payload)
    assert created_token.check_status_is_(404)


@allure.description('Check token status')
@allure.feature('a. Authorization')
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
@allure.feature('a. Authorization')
@allure.story('08. Check incorrect token')
@allure.title('GET /authorize/incorrect token')
@pytest.mark.regression
def test_incorrect_token(checked_token):
    checked_token.check_incorrect_token_status()
    assert checked_token.check_status_is_(404)


@allure.description('Check token with wrong methods')
@allure.feature('a. Authorization')
@allure.story('09. Wrong token checking')
@allure.title('non-GET /authorize/token')
@pytest.mark.parametrize('method', ['POST', 'PATCH', 'PUT', 'DELETE'])
@pytest.mark.regression
def test_wrong_checking_token_url(checked_token, user_token, method):
    checked_token.wrong_method(method, user_token)
    assert checked_token.check_status_is_(405)


@allure.description('Check obsolete token')
@allure.feature('a. Authorization')
@allure.story('10. Check obsolete token')
@allure.title('GET /authorize/obsolete token')
@pytest.mark.regression
def test_obsolete_token(checked_token):
    checked_token.check_obsolete_token(obs_token)
    assert checked_token.check_status_is_(404)


@allure.description('Check token with wrong url')
@allure.feature('a. Authorization')
@allure.story('11. Check token with wrong url')
@allure.title('GET /wrong url/token')
@pytest.mark.regression
def test_token_with_wrong_url(user_token, checked_token):
    checked_token.check_token_with_wrong_url(user_token)
    assert checked_token.check_status_is_(404)


@allure.description('Fetch all memes')
@allure.feature('b. Get Memes')
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
@allure.feature('b. Get Memes')
@allure.story('13. Wrong get memes without token')
@allure.title('GET /meme without token')
@pytest.mark.regression
def test_get_memes_without_token(fetch_all_memes):
    fetch_all_memes.fetch_memes_without_token()
    assert fetch_all_memes.check_status_is_(401)


@allure.description('Fetch memes with incorrect tokens')
@allure.feature('b. Get Memes')
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
@allure.feature('b. Get Memes')
@allure.story('15. Wrong methods for getting memes')
@allure.title('non-GET /meme')
@pytest.mark.parametrize('method', ['PATCH', 'PUT', 'DELETE'])
@pytest.mark.regression
def test_wrong_methods_for_getting_memes(fetch_all_memes, user_token, method):
    fetch_all_memes.wrong_method(method, user_token)
    assert fetch_all_memes.check_status_is_(405)


@allure.description('Check single meme by ID')
@allure.feature('b. Get Memes')
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
@allure.feature('b. Get Memes')
@allure.story('17. Get meme by incorrect ID')
@allure.title('GET /meme/incorrect id')
@pytest.mark.parametrize('id', [2, 0, '', ' ', -1, '01', 'a', '*', 1.5])
@pytest.mark.regression
def test_get_meme_by_incorrect_id(fetch_meme, user_token, test_id):
    header = fetch_meme.auth_header(user_token)
    fetch_meme.fetch_meme_by_id_without_json(header, test_id)
    assert fetch_meme.check_status_is_(404)

@allure.description('Check single meme without token')
@allure.feature('b. Get Memes')
@allure.story('18. Get meme without token')
@allure.title('GET /meme/id')
@pytest.mark.regression
def test_get_meme_without_token(fetch_meme, meme_id):
    header = fetch_meme.non_auth_header
    fetch_meme.fetch_meme_by_id_without_json(header, meme_id)
    assert fetch_meme.check_status_is_(401)

@allure.description('Check single meme by ID with incorrect token')
@allure.feature('b. Get Memes')
@allure.story('19. Get meme by ID with incorrect token')
@allure.title('GET /meme/id')
@pytest.mark.parametrize('token', ['1', 'token', obs_token])  # , '', ' ' добавить пустую строку и пробед (они пятисотят почему-то
@pytest.mark.regression
def test_get_meme_with_incorrect_token(fetch_meme, token, meme_id):
    header = fetch_meme.auth_header(token)
    fetch_meme.fetch_meme_by_id_without_json(header, meme_id)
    assert fetch_meme.check_status_is_(401)

@allure.description('Check single meme with incorrect method')
@allure.feature('b. Get Memes')
@allure.story('20. Wrong methods for getting single meme by ID')
@allure.title('non-GET /meme/id')
@pytest.mark.parametrize('method', ['POST', 'PATCH'])
@pytest.mark.regression
def test_get_meme_with_incorrect_method(fetch_meme, user_token, meme_id, method):
    header = fetch_meme.auth_header(user_token)
    fetch_meme.fetch_meme_with_incorrect_method(header, meme_id, method)
    assert fetch_meme.check_status_is_(405)

@allure.description('Creating new meme')
@allure.feature('c. Create Memes')
@allure.story('21. Meme creation')
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

@allure.description('Creating new meme without token')
@allure.feature('c. Create Memes')
@allure.story('22. Meme creation without token')
@allure.title('POST /meme without token')
@pytest.mark.regression
def test_creation_meme_without_token(creating_meme):
    header = creating_meme.non_auth_header
    creating_meme.create_meme_without_json(header, meme_creation_payload)
    assert creating_meme.check_status_is_(401)

@allure.description('Creating empty meme')
@allure.feature('c. Create Memes')
@allure.story('23. Meme creation without any data')
@allure.title('POST /empty meme')
@pytest.mark.regression
def test_creation_empty_meme(creating_meme, user_token):
    header = creating_meme.auth_header(user_token)
    creating_meme.create_meme_without_json(header, part_of_payload)
    assert creating_meme.check_status_is_(200)  # Я бы завел баг или порекомендовал доработку на валидацию

@allure.description('Creating meme without required field')
@allure.feature('c. Create Memes')
@allure.story('24. Meme creation without one field')
@allure.title('POST /meme without one field')
@pytest.mark.parametrize('field', [pwf[0], pwf[1], pwf[2], pwf[3]])
@pytest.mark.regression
def test_creation_meme_without_field(creating_meme, user_token, field):
    header = creating_meme.auth_header(user_token)
    creating_meme.create_meme_without_json(header, field)
    assert creating_meme.check_status_is_(400)

@allure.description('Creating meme with incorrect data types')
@allure.feature('c. Create Memes')
@allure.story('25. Meme creation with incorrect data types')
@allure.title('POST /meme with incorrect data types')
@pytest.mark.parametrize('field', ['text', 'tags', 'url', 'info'])
@pytest.mark.parametrize('data', [10, False, None, 0.25, ])
@pytest.mark.regression
def test_creation_meme_with_incorrect_data_types(creating_meme, user_token, field, data):
    header = creating_meme.auth_header(user_token)
    creating_meme.create_meme_with_different_data(header, part_of_payload, field, data)
    assert creating_meme.check_status_is_(400)

@allure.description('Deleting meme')
@allure.feature('d. Delete Meme')
@allure.story('26. Meme deletion')
@allure.title('DELETE /meme')
@pytest.mark.smoke
@pytest.mark.regression
def test_deletion_meme(deleting_meme, user_token, meme_id):
    header = deleting_meme.auth_header(user_token)
    deleting_meme.delete_meme(header, meme_id)
    assert deleting_meme.check_status_is_(200)
    assert deleting_meme.check_correct_text_in_response()
    assert deleting_meme.check_id_is_correct(meme_id)

@allure.description('Deleting meme without token')
@allure.feature('d. Delete Meme')
@allure.story('27. Meme deletion without token')
@allure.title('DELETE /meme without token')
@pytest.mark.regression
def test_deletion_meme_without_token(deleting_meme, meme_id, user_token):
    header = deleting_meme.non_auth_header
    deleting_meme.delete_meme(header, meme_id)
    assert deleting_meme.check_status_is_(401)
    assert deleting_meme.check_mem_is_exist_after_wrong_deletion(user_token, meme_id)

@allure.description('Deleting meme by incorrect ID')
@allure.feature('d. Delete Meme')
@allure.story('28. Meme deletion by incorrect ID')
@allure.title('DELETE /meme by incorrect ID')
@pytest.mark.regression
def test_deletion_meme_by_incorrect_id(deleting_meme, user_token):
    header = deleting_meme.auth_header(user_token)
    deleting_meme.delete_meme(header, 0)
    assert deleting_meme.check_status_is_(404)

@allure.description('Deleting deleted meme')
@allure.feature('d. Delete Meme')
@allure.story('29. Meme twice deletion')
@allure.title('DELETE /meme again')
@pytest.mark.regression
def test_deletion_meme_twice(deleting_meme, user_token, meme_id):
    header = deleting_meme.auth_header(user_token)
    deleting_meme.delete_meme(header, meme_id)
    deleting_meme.delete_meme(header, meme_id)
    assert deleting_meme.check_status_is_(404)

@allure.description('Deleting another users meme')
@allure.feature('d. Delete Meme')
@allure.story('30. Foreign meme deletion')
@allure.title('DELETE /foreign meme')
@pytest.mark.regression
def test_deletion_foreign_meme(deleting_meme, another_user_token, meme_id):
    header = deleting_meme.auth_header(another_user_token)
    deleting_meme.delete_meme(header, meme_id)
    assert deleting_meme.check_status_is_(403)

@allure.description('Changing meme')
@allure.feature('e. Change Meme')
@allure.story('31. Changing meme')
@allure.title('PUT /meme/id')
@pytest.mark.smoke
@pytest.mark.regression
def test_changing_meme(change_meme, user_token, meme_id):
    header = change_meme.auth_header(user_token)
    change_meme.change_meme(header, new_meme_payload, meme_id)
    assert change_meme.check_status_is_(200)
    assert change_meme.check_response_is_correct(new_meme_payload, meme_id)
    assert change_meme.sure_correct_changes_is_in_db(header, user_token, meme_id)

@allure.description('Changing meme whithout token')
@allure.feature('e. Change Meme')
@allure.story('32. Changing meme  whithout token')
@allure.title('PUT /meme/id whithout token')
@pytest.mark.regression
def test_changing_meme_without_token(change_meme, meme_id):
    header = change_meme.non_auth_header
    change_meme.change_meme_without_json(header, new_meme_payload, meme_id)
    assert change_meme.check_status_is_(401)

@allure.description('Changing meme without required field')
@allure.feature('e. Change Meme')
@allure.story('33. Changing meme without one field')
@allure.title('PUT /meme/id without one field')
@pytest.mark.parametrize('field', [pwf[0], pwf[1], pwf[2], pwf[3], pwf[4]])
@pytest.mark.regression
def test_changing_meme_without_field(change_meme, user_token, meme_id, field):
    header = change_meme.auth_header(user_token)
    change_meme.change_meme_without_json(header, field, meme_id)
    assert change_meme.check_status_is_(400)


@allure.description('Changing meme with incorrect data types')
@allure.feature('e. Change Meme')
@allure.story('34. Changing meme with incorrect data types')
@allure.title('PUT /meme/id with incorrect data types')
@pytest.mark.parametrize('field', ['id', 'text', 'tags', 'url', 'info'])
@pytest.mark.parametrize('data', [10, False, None, 0.25, ])
@pytest.mark.regression
def test_changing_meme_with_incorrect_data_types(change_meme, user_token, meme_id, field, data):
    header = change_meme.auth_header(user_token)
    change_meme.update_meme_with_different_data(header, new_meme_payload, meme_id, field, data)
    assert change_meme.check_status_is_(400)

@allure.description('Changing meme with different ID')
@allure.feature('e. Change Meme')
@allure.story('35. Changing meme with different ID')
@allure.title('PUT /meme/id with different ID')
@pytest.mark.regression
def test_changing_meme_with_different_id(change_meme, user_token, meme_id):
    header = change_meme.auth_header(user_token)
    change_meme.change_meme_with_different_id(header, new_meme_payload, meme_id)
    assert change_meme.check_status_is_(400)

@allure.description('Changing meme with nonexistent ID')
@allure.feature('e. Change Meme')
@allure.story('36. Changing meme with nonexistent ID')
@allure.title('PUT /meme/id with nonexistent ID')
@pytest.mark.regression
def test_changing_meme_with_nonexistent_id(change_meme, user_token, meme_id):
    id = meme_id + 100000
    header = change_meme.auth_header(user_token)
    change_meme.change_meme_without_json(header, new_meme_payload, id)
    assert change_meme.check_status_is_(404)

@allure.description('Changing another users meme')
@allure.feature('e. Change Meme')
@allure.story('37Ж::. Foreign meme changing')
@allure.title('PUT /foreign meme')
@pytest.mark.regression
def test_changing_foreign_meme(change_meme, another_user_token, meme_id):
    header = change_meme.auth_header(another_user_token)
    change_meme.change_meme_without_json(header, new_meme_payload, meme_id)
    assert change_meme.check_status_is_(403)
