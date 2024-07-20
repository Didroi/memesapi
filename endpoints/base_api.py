import allure
import requests
import os


class BaseApi:
    response: requests.Response
    response_json: dict
    non_auth_header = {'Content-Type': 'application/json'}
    obsolete_token = 'zD5qoUYJDD3Glgy'

    @allure.step('Check status code')
    def check_status_is_(self, code):
        return self.response.status_code == code

    @staticmethod
    def active_token():
        file_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)
                            ), 'tests', 'data', 'token.txt'
        )
        with open(file_path, 'r', encoding='utf-8') as f:
            token = f.readline().rstrip('\n')
        return token

    @staticmethod
    def auth_header(token):
        header = {'Content-Type': 'application/json', 'authorization': token}
        return header
