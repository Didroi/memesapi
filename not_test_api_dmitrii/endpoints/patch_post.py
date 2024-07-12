import requests
import allure
from tests import BaseApi
from tests import headers as h
from tests import url


class PatchPost(BaseApi):
    @allure.step('Partially update Post')
    def patch_post(self, object_id, payload, header=None):
        headers = header if header else h.headers_temp

        self.response = requests.put(
            f'{url.url}/{object_id}',
            json=payload,
            headers=headers
        )

        self.response_json = self.response.json()

    @allure.step('Check right hard disk size in response')
    def check_correct_(self, key, value):
        return self.response_json['data'][key] == value
