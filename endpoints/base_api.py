import allure
import requests


class BaseApi:
    response: requests.Response
    response_json: dict
    token: str

    @allure.step('Check status code')
    def check_status_is_(self, code):
        return self.response.status_code == code

    @allure.step('Check whithout Token')
    def try_without_token(self, name):
        pass

