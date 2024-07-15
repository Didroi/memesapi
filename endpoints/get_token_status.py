import requests
import allure
from tests.data import headers as h
from tests.data import url
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



    @allure.step('Check correct answer')
    def check_correct_text_in_request(self):
        return 'Token is alive.' in self.response_txt

    @allure.step('Check token in response')
    def check_response_has_token(self):
        return 'token' in self.response_json

