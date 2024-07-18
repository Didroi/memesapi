import requests
import allure
from tests.data import headers as h
from tests.data import url
from tests.data import token as t
from endpoints.base_api import BaseApi


class CreateToken(BaseApi):
    @allure.step('Create Token')
    def create_token(self, payload, header=None):
        headers = header if header else h.non_auth_header

        self.response = requests.post(
            f'{url.url}/authorize',
            json=payload,
            headers=headers
        )

        self.response_json = self.response.json()
        self.token = self.response_json['token']

    @allure.step('Update Token in files')
    def update_token_in_file(self):
        file_path = t.path
        with open(file_path, 'r') as f:
            lines = f.readlines()
        lines[5] = f'    "active token": "{self.token}",\n'
        with open(file_path, 'w') as f:
            f.writelines(lines)

    @allure.step('Create Token')
    def false_create_token(self, payload, header=None):
        headers = header if header else h.non_auth_header

        self.response = requests.post(
            f'{url.url}/authorize',
            json=payload,
            headers=headers
        )

    @allure.step('Wrong method')
    def wrong_method(self, payload, method, header=None):
        headers = header if header else h.non_auth_header

        self.response = requests.request(str(method),
                                         f'{url.url}/authorize',
                                         json=payload,
                                         headers=headers
                                         )

    @allure.step('Wrong URL')
    def wrong_url(self, payload, header=None):
        headers = header if header else h.non_auth_header

        self.response = requests.post(
            f'{url.url}/404authorize',
            json=payload,
            headers=headers
        )

    @allure.step('Check response Name')
    def check_response_user_is_(self, user):
        return self.response_json['user'] == user

    @allure.step('Check token in response')
    def check_response_has_token(self):
        return 'token' in self.response_json
