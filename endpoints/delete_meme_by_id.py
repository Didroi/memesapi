import requests
import allure
from tests.data import url
from endpoints.base_api import BaseApi
from endpoints.get_meme_by_id import SingleMemeFetcher


class MemeAnnihilator(BaseApi):
    @allure.step('Delete meme by ID')
    def delete_meme(self, header, deletion_id):

        self.response = requests.delete(
            f'{url.url}/meme/{deletion_id}',
            headers=header
        )
        self.response_txt = self.response.text

    @allure.step('Check correct answer')
    def check_correct_text_in_response(self):
        return 'successfully deleted' in self.response_txt

    @allure.step('Check user is correct')
    def check_id_is_correct(self, checking_id):
        return str(checking_id) in self.response_txt

    @allure.step('Check meme is exist')
    def check_mem_is_exist_after_wrong_deletion(self, token, checking_id):
        checking_meme = SingleMemeFetcher()
        header = checking_meme.auth_header(token)
        get_meme_by_id = checking_meme.fetch_meme_by_id(header, checking_id)
        return get_meme_by_id['id'] == checking_id
