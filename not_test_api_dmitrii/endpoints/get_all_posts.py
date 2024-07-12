import requests
import allure
from tests import BaseApi
from tests import url


class GetPosts(BaseApi):
    @allure.step('Get all Posts')
    def get_posts(self):

        self.response = requests.get(
            url.url
        )
