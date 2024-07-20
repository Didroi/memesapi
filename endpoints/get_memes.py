import requests
import allure
from tests.data import url
from endpoints.base_api import BaseApi


class MemesFetcher(BaseApi):
    @allure.step('Fetch all memes')
    def fetch_all_memes(self, header):

        self.response = requests.get(
            f'{url.url}/meme',
            headers=header
        )

        self.response_json = self.response.json()

    @allure.step('Check memes with wrong methods')
    def wrong_method(self, method, token):

        self.response = requests.request(str(method), f'{url.url}/meme',
                                         headers=self.auth_header(token))

    @allure.step('Fetch memes without token')
    def fetch_memes_without_token(self):

        self.response = requests.get(
            f'{url.url}/meme',
            headers=self.non_auth_header
        )

    @allure.step('Fetch memes with incorrect token')
    def fetch_memes_with_incorrect_token(self, token):

        self.response = requests.get(
            f'{url.url}/meme',
            headers=self.auth_header(token)
        )

        self.sending_header = self.auth_header(token)

    @allure.step('Check sending correct data in token')
    def check_sending_token_is_right(self, sending_token):
        return self.sending_header['authorization'] == sending_token

    @allure.step('Check data in answer and it is not empty')
    def check_data_is_not_empty(self):
        return self.response_json['data']

    @allure.step('Checking unique IDs')
    def check_unique_ids(self):
        ids_list = []
        for element in self.response_json['data']:
            if element['id'] in ids_list:
                return False
            ids_list.append(element['id'])
        return True
