import requests
import allure
from tests import BaseApi
from tests import url


class GetPost(BaseApi):
    @allure.step('Get created Post')
    def get_post(self, object_id):

        self.response = requests.get(
            f'{url.url}/{object_id}'
        )

        self.response_json = self.response.json()
