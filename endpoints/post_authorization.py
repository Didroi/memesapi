import requests
import allure
from tests.data import headers as h
from tests.data import url
from endpoints.base_api import BaseApi


class CreateToken(BaseApi):
    @allure.step('Create Token')
    def create_token(self, payload, header=None):
        headers = header if header else h.header

        self.response = requests.post(
            f'{url.url}/authorize',
            json=payload,
            headers=headers
        )

        self.response_json = self.response.json()
        self.token = self.response_json['token']
        # print(self.response_json)
        # print(self.token)


