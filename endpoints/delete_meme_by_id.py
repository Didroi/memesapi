import requests
import allure
from tests.data import url
from endpoints.base_api import BaseApi


class MemeAnnihilator(BaseApi):
    @allure.step('Delete meme by ID')
    def delete_meme(self, header, id):

        self.response = requests.delete(
            f'{url.url}/meme/{id}',
            headers=header
        )
        # self.response_txt = self.response.json()

    def check_correct_id_in_response(self, id):
        return self.response_json['id'] == id

    @allure.step('Fetch single meme by ID')
    def fetch_meme_by_id_without_json(self, header, id):

        self.response = requests.get(
            f'{url.url}/meme/{id}',
            headers=header
        )
