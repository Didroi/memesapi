import pytest
import allure
from tests import payloads


name_of_created_supply = payloads.payload_for_creation['name']
name_of_updated_supply = payloads.payload_for_update['name']
name_of_part_updated_supply = payloads.payload_for_partially_update['name']


@allure.description('Check creating Post')
@allure.feature('With one object')
@allure.story('POST')
@allure.title('Create Post')
@pytest.mark.regression
def test_create_object(follow_the_testing_without_object, create_object):
    create_object.create_object(payloads.payload_for_creation)
    assert create_object.check_status_is_(200)
    assert create_object.check_response_name_is_(name_of_created_supply)


@allure.description('Check deleting Post')
@allure.feature('With one object')
@allure.story('DEL')
@allure.title('Delete Post')
@pytest.mark.regression
def test_delete_object(deleted_object, object_id):
    deleted_object.delete_object(object_id)
    assert deleted_object.check_status_is_(200)
    assert deleted_object.deletion_confirm()


@allure.description('Check created Post')
@allure.feature('With one object')
@allure.story('GET')
@allure.title('Watch Post')
@pytest.mark.regression
@pytest.mark.smoke
def test_get_object(object_id, get_object):
    get_object.get_post(object_id)
    assert get_object.check_status_is_(200)
    assert get_object.check_response_name_is_(name_of_created_supply)


@allure.description('Check all Posts')
@allure.feature('All objects')
@allure.story('GET')
@allure.title('Watch all Posts')
@pytest.mark.regression
@pytest.mark.smoke
def test_get_all_object(follow_the_testing_without_object, get_objects):
    get_objects.get_posts()
    assert get_objects.check_status_is_(200)


@allure.description('Check updating Post')
@allure.feature('With one object')
@allure.story('PUT')
@allure.title('Change Post')
@pytest.mark.parametrize('price', [199.9, '297.3', -100, 'handred bucks'])
@pytest.mark.regression
@pytest.mark.critical
def test_update_object(object_id, price, update_object):
    update_object.put_post(object_id, payloads.payload_for_update)
    assert update_object.check_status_is_(200)
    assert update_object.check_response_name_is_(name_of_updated_supply)


@allure.description('Check partially updating Post')
@allure.feature('With one object')
@allure.story('PATCH')
@allure.title('Cnahge the part of Post')
@pytest.mark.parametrize('key', ['Hard disk size', 'price'])
@pytest.mark.regression
def test_partually_update_object(object_id, partially_update_object, key):
    partially_update_object.patch_post(object_id, payloads.payload_for_partially_update)
    assert partially_update_object.check_status_is_(200)
    assert partially_update_object.check_response_name_is_(name_of_part_updated_supply)
    assert partially_update_object.check_correct_(key, payloads.payload_for_partially_update['data'][key])
