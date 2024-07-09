import requests
import pytest
from endpoints.post_authorization import CreateToken


@pytest.fixture()
def object_id():
    print('Start testing')
    create_object = PostPost()
    create_object.create_object(payloads.payload_for_creation)
    obj_id = create_object.response_json['id']
    yield obj_id
    requests.delete(f'https://api.restful-api.dev/objects/{obj_id}')
    print('Testing completed')


@pytest.fixture()
def follow_the_testing_without_object():
    print('Start testing')
    yield
    print('Testing completed')


# @pytest.fixture()
# def deleted_object():
#     return DeletePost()


@pytest.fixture()
def created_token():
    return CreateToken()


