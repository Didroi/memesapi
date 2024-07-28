import requests
import allure
from tests.data import url
from endpoints.base_api import BaseApi


class SingleMemeFetcher(BaseApi):
    @allure.step('Fetch single meme by ID')
    def fetch_meme_by_id(self, header, checking_id):

        self.response = requests.get(
            f'{url.url}/meme/{checking_id}',
            headers=header
        )

        self.response_json = self.response.json()
        return self.response_json

    def check_correct_id_in_response(self, checking_id):
        return self.response_json['id'] == checking_id

    @allure.step('Fetch single meme by ID')
    def fetch_meme_by_id_without_json(self, header, checking_id):

        self.response = requests.get(
            f'{url.url}/meme/{checking_id}',
            headers=header
        )

    @allure.step('Check single meme with incorrect method')
    def fetch_meme_with_incorrect_method(self, header, checking_id, method):

        self.response = requests.request(
            method,
            f'{url.url}/meme/{checking_id}',
            headers=header
        )
