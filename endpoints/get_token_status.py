import requests
import allure
from tests.data import headers as h
from tests.data import url
from endpoints.base_api import BaseApi
from tests.data import token as t

class CheckTokenStatus(BaseApi):
    @allure.step('Check Token status')
    def check_token_status(self, user_token, header=None):
        headers = header if header else h.non_auth_header

        self.response = requests.get(
            f'{url.url}/authorize/{user_token}',
            headers=headers
        )

        self.response_txt = self.response.text




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
        print()
        print(self.response_json)
        print(t.token)
        print(t.token in self.response_json)
        return t.token in self.response_json

    @allure.step('Check correct text in response')
    def check_response_has_correct_text(self):
        return 'Token is alive. Username is' in self.response_json
