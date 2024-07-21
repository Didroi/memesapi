import requests
import allure
from tests.data import url
from endpoints.base_api import BaseApi


class MemeCreator(BaseApi):
    @allure.step('Creating new meme')
    def create_meme(self, header, payload):

        self.response = requests.post(
            f'{url.url}/meme',
            json=payload,
            headers=header
        )

        self.response_json = self.response.json()
        return self.response_json['id']

    def check_correct_id_in_response(self, id):
        return self.response_json['id'] == id

    @allure.step('Fetch single meme by ID')
    def fetch_meme_by_id_without_json(self, header, id):

        self.response = requests.get(
            f'{url.url}/meme/{id}',
            headers=header
        )
