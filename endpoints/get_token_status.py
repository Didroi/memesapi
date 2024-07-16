import requests
import allure
from tests.data import headers as h
from tests.data import url
# from tests.data import payloads as p
from endpoints.base_api import BaseApi


class CheckTokenStatus(BaseApi):
    @allure.step('Check Token status')
    def check_token_status(self, user_token, header=None):
        headers = header if header else h.non_auth_header

        self.response = requests.get(
            f'{url.url}/authorize/{user_token}',
            headers=headers
        )

        self.response_txt = self.response.text

    @allure.step('Check incorrect Token status')
    def check_incorrect_token_status(self, header=None):
        headers = header if header else h.non_auth_header

        self.response = requests.get(
            f'{url.url}/authorize/incorrect_token'
        )

    @allure.step('Wrong method')
    def wrong_method(self, method, user_token, header=None):
        headers = header if header else h.non_auth_header

        self.response = requests.request(str(method),
                                         f'{url.url}/authorize/{user_token}',
                                         headers=headers
                                         )

    @allure.step('Check correct answer')
    def check_correct_text_in_request(self):
        return 'Token is alive.' in self.response_txt

    @allure.step('Check user is correct')
    def check_user_is_correct(self, user):
        return user in self.response_txt

