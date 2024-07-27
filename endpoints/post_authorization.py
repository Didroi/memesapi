import requests
import allure
import os
from tests.data import url
from endpoints.base_api import BaseApi


class CreateToken(BaseApi):
    @allure.step('Create Token')
    def create_token(self, payload):
        self.response = requests.post(
            f'{url.url}/authorize',
            json=payload,
            headers=self.non_auth_header
        )

        self.response_json = self.response.json()
        self.token = self.response_json['token']

    @allure.step('Update Token in files')
    def update_token_in_file(self):
        file_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)
                            ), 'tests', 'data', 'token.txt'
        )
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(self.token)

    @allure.step('Create Token')
    def false_create_token(self, payload):
        self.response = requests.post(
            f'{url.url}/authorize',
            json=payload,
            headers=self.non_auth_header
        )

    @allure.step('Wrong method')
    def wrong_method(self, payload, method):

        self.response = requests.request(str(method),
                                         f'{url.url}/authorize',
                                         json=payload,
                                         headers=self.non_auth_header
                                         )

    @allure.step('Wrong URL')
    def wrong_url(self, payload):
        self.response = requests.post(
            f'{url.url}/404authorize',
            json=payload,
            headers=self.non_auth_header
        )

    @allure.step('Check response Name')
    def check_response_user_is_(self, user):
        return self.response_json['user'] == user

    @allure.step('Check token in response')
    def check_response_has_token(self):
        return 'token' in self.response_json
