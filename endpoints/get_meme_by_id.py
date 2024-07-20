import requests
import allure
from tests.data import url
from endpoints.base_api import BaseApi


class SingleMemeFetcher(BaseApi):
    @allure.step('Fetch single meme by ID')
    def fetch_meme_by_id(self, header, id):

        self.response = requests.get(
            f'{url.url}/meme/{id}',
            headers=header
        )

        self.response_json = self.response.json()
