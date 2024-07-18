import requests
import allure
from tests.data import headers as h
from tests.data import url
# from tests.data import payloads as p
from endpoints.base_api import BaseApi


class MemesFetcher(BaseApi):
    @allure.step('Fetch all memes')
    def fetch_all_memes(self, header=None):
        headers = header if header else h.auth_header

        self.response = requests.get(
            f'{url.url}/meme',
            headers=headers
        )
        print(headers)
        self.response_json = self.response.json()
        print(self.response_json)
        print(self.response)

    # @allure.step('Check user is correct')
    # def check_user_is_correct(self, user):
    #     return user in self.response_txt
