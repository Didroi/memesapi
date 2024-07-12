import requests
import allure
from tests import BaseApi
from tests import headers as h
from tests import url


class PostPost(BaseApi):
    @allure.step('Create Post')
    def create_object(self, payload, header=None):
        headers = header if header else h.headers_temp

        self.response = requests.post(
            url.url,
            json=payload,
            headers=headers
        )

        self.response_json = self.response.json()
