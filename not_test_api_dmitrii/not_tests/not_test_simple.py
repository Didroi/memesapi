import allure
import pytest


@allure.description('Check skipping test')
@allure.feature('Simple test')
@allure.story('Equals')
@allure.title('Simple test')
def test_for_simple_check(follow_the_testing_without_object, small_checks):
    assert small_checks.correct_equals()


@allure.description('Check skipping test')
@allure.feature('Simple test')
@allure.story('Equals')
@allure.title('Skipping test')
@pytest.mark.skip(reason='Teacher said')
def test_to_skip(follow_the_testing_without_object, small_checks):
    assert small_checks.correct_equals()


@allure.description('Check failing test')
@allure.feature('Simple test')
@allure.story('Equals')
@allure.title('Failing test')
@pytest.mark.smoke
def test_to_failing(follow_the_testing_without_object, small_checks):
    assert small_checks.incorrect_equals()
