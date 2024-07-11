import pytest
from endpoints.post_authorization import CreateToken


# @pytest.fixture()
# def delete_


@pytest.fixture()
def created_token():
    return CreateToken()
