import requests
import pytest
from endpoints import payloads
from endpoints import DeletePost
from endpoints import PostPost
from endpoints import GetPosts
from endpoints import GetPost
from endpoints import PutPost
from endpoints import PatchPost
from endpoints import SmallChecks


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


@pytest.fixture()
def deleted_object():
    return DeletePost()


@pytest.fixture()
def create_object():
    return PostPost()


@pytest.fixture()
def get_objects():
    return GetPosts()


@pytest.fixture()
def get_object():
    return GetPost()


@pytest.fixture()
def update_object():
    return PutPost()


@pytest.fixture()
def partially_update_object():
    return PatchPost()


@pytest.fixture()
def small_checks():
    return SmallChecks()
