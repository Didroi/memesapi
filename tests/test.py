import pytest
import allure
from tests.data import payloads as p


user = p.token_payload['name']


@allure.description('description')
@allure.feature('feature')
@allure.story('story')
@allure.title('title')
@pytest.mark.regression
def test_create_token(created_token):
    created_token.create_token(p.token_payload)
    assert created_token.check_status_is_(200)
    assert created_token.check_response_user_is_(user)

