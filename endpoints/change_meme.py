import requests
import allure
from tests.data import url
from endpoints.base_api import BaseApi
from endpoints.get_meme_by_id import SingleMemeFetcher


class MemeChanger(BaseApi):
    @allure.step('Changing meme')
    def change_meme(self, header, payload, change_id):
        payload['id'] = change_id

        self.response = requests.put(
            f'{url.url}/meme/{change_id}',
            json=payload,
            headers=header
        )

        # self.updated_payload = payload
        self.response_json = self.response.json()
        # self.header = header
        # return self.response_json['id']

    def change_meme_without_json(self, header, payload, change_id):
        if 'id' in payload:
            payload['id'] = change_id

        self.response = requests.put(
            f'{url.url}/meme/{change_id}',
            json=payload,
            headers=header
        )

    @allure.step('Check changing response')
    def check_response_is_correct(self, payload, change_id):
        id_is_correct = self.response_json['id'] == str(change_id)
        text_is_correct = self.response_json['text'] == payload['text']
        tags_is_correct = self.response_json['tags'] == payload['tags']
        url_is_correct = self.response_json['url'] == payload['url']
        info_is_correct = self.response_json['info'] == payload['info']
        return text_is_correct and id_is_correct and tags_is_correct and url_is_correct and info_is_correct

    @allure.step('Check changing meme is correct')
    def sure_correct_changes_is_in_db(self, header, change_id):
        checking_meme = SingleMemeFetcher()
        get_meme_by_id = checking_meme.fetch_meme_by_id(header, change_id)
        return get_meme_by_id == self.response_json

    @allure.step('Changing meme with incorrect data types')
    def update_meme_with_different_data(self, header, original_payload, change_id, field, data):
        payload = original_payload.copy()
        payload['id'] = change_id
        payload[field] = data

        self.response = requests.put(
            f'{url.url}/meme/{change_id}',
            json=payload,
            headers=header
        )

    def change_meme_with_different_id(self, header, payload, change_id):
        if 'id' in payload:
            payload['id'] = change_id - 1

        self.response = requests.put(
            f'{url.url}/meme/{change_id}',
            json=payload,
            headers=header
        )
