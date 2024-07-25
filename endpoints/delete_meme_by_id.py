import requests
import allure
from tests.data import url
from endpoints.base_api import BaseApi
from endpoints.get_meme_by_id import SingleMemeFetcher


class MemeAnnihilator(BaseApi):
    @allure.step('Delete meme by ID')
    def delete_meme(self, header, id):

        self.response = requests.delete(
            f'{url.url}/meme/{id}',
            headers=header
        )
        self.response_txt = self.response.text

    # @allure.step('Delete meme by ID')
    # def delete_meme_without_response_text(self, header, id):
    #
    #     self.response = requests.delete(
    #         f'{url.url}/meme/{id}',
    #         headers=header
    #     )

    @allure.step('Check correct answer')
    def check_correct_text_in_response(self):
        return 'successfully deleted' in self.response_txt

    @allure.step('Check user is correct')
    def check_id_is_correct(self, id):
        return str(id) in self.response_txt

    @allure.step('Check meme is exist')
    def check_mem_is_exist_after_wrong_deletion(self, token, id):
        checking_meme = SingleMemeFetcher()
        header = checking_meme.auth_header(token)
        get_meme_by_id = checking_meme.fetch_meme_by_id(header, id)
        return get_meme_by_id['id'] == id
