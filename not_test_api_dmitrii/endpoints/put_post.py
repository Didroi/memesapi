import requests
import allure
from tests import BaseApi
from tests import headers as h
from tests import url


class PutPost(BaseApi):
    @allure.step('Update Post')
    def put_post(self, object_id, payload, header=None):
        headers = header if header else h.headers_temp

        self.response = requests.put(
            f'{url.url}/{object_id}',
            json=payload,
            headers=headers
        )

        self.response_json = self.response.json()
