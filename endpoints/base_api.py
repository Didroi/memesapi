import allure
import requests


class BaseApi:
    response: requests.Response
    response_json: dict

    @allure.step('Check status code')
    def check_status_is_(self, code):
        return self.response.status_code == code

    @allure.step('Check response Name')
    def check_response_user_is_(self, user):
        return self.response_json['user'] == user

    @allure.step('Check whithout Token')
    def try_without_token(self, name):
        pass
