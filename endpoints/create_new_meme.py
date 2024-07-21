import requests
import allure
from tests.data import url
from endpoints.base_api import BaseApi
from endpoints.delete_meme_by_id import MemeAnnihilator


class MemeCreator(BaseApi):
    @allure.step('Creating new meme')
    def create_meme(self, header, payload):

        self.response = requests.post(
            f'{url.url}/meme',
            json=payload,
            headers=header
        )

        self.response_json = self.response.json()
        self.header = header
        return self.response_json['id']

    def check_id_in_response(self):
        print(self.response_json['id'])
        return self.response_json['id'] > 0

    def delete_meme_after_creating(self):
        delete_obj = MemeAnnihilator()
        delete_obj.delete_meme(self.header, self.response_json['id'])
    #
    # @allure.step('Fetch single meme by ID')
    # def fetch_meme_by_id_without_json(self, header, id):
    #
    #     self.response = requests.get(
    #         f'{url.url}/meme/{id}',
    #         headers=header
    #     )
