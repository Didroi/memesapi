import requests
import allure
# from tests.data import headers as h
from tests.data import url
from endpoints.base_api import BaseApi


class CheckTokenStatus(BaseApi):
    @allure.step('Check Token status')
    def check_token_status(self, token):
        self.response = requests.get(
            f'{url.url}/authorize/{token}',
            headers=self.non_auth_header
        )

        self.response_txt = self.response.text

    @allure.step('Check incorrect Token status')
    def check_incorrect_token_status(self):
        self.response = requests.get(
            f'{url.url}/authorize/incorrect_token'
        )

    @allure.step('Wrong method')
    def wrong_method(self, method, token):
        self.response = requests.request(str(method), f'{url.url}/authorize/{token}',
                                         headers=self.non_auth_header)

    @allure.step('Check obsolete Token')
    def check_obsolete_token(self, token):
        self.response = requests.get(
            f'{url.url}/authorize/{token}',
            headers=self.non_auth_header
        )

        self.response_txt = self.response.text

    @allure.step('Check Token with wrong url')
    def check_token_with_wrong_url(self, user_token):
        self.response = requests.get(
            f'{url.url}/avthorizec/{user_token}',
            headers=self.non_auth_header
        )

        self.response_txt = self.response.text

    @allure.step('Check correct answer')
    def check_correct_text_in_request(self):
        return 'Token is alive.' in self.response_txt

    @allure.step('Check user is correct')
    def check_user_is_correct(self, user):
        return user in self.response_txt
