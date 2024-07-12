import allure
import requests


class BaseApi:
    response: requests.Response
    response_json: dict

    @allure.step('Check status code')
    def check_status_is_(self, code):
        return self.response.status_code == code

    @allure.step('Check response Name')
    def check_response_name_is_(self, name):
        return self.response_json['name'] == name
