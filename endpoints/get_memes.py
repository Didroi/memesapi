import requests
import allure
from tests.data import headers as h
from tests.data import url
from endpoints.base_api import BaseApi


class MemesFetcher(BaseApi):
    @allure.step('Fetch all memes')
    def fetch_all_memes(self, header=None):
        headers = header if header else h.auth_header

        self.response = requests.get(
            f'{url.url}/meme',
            headers=headers
        )

        self.response_json = self.response.json()

    @allure.step('Fetch memes without token')
    def fetch_memes_without_token(self, header=None):
        headers = header if header else h.non_auth_header

        self.response = requests.get(
            f'{url.url}/meme',
            headers=headers
        )


    @allure.step('Check data in answer and not empty')
    def check_data_is_not_empty(self):
        return self.response_json['data']

    @allure.step('Checking unique IDs')
    def check_unique_ids(self):
        # print()
        ids_list = []
        for object in self.response_json['data']:
            if object['id'] in ids_list:
                return False
            ids_list.append(object['id'])
        return True
